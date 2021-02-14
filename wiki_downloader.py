"""
Author: Alex Hedges
"""

import argparse
import bz2
import json
import os
import re
import xml.etree.ElementTree as ET
from io import StringIO
from os.path import splitext
from urllib import request
from urllib.parse import urljoin

from gensim.corpora import wikicorpus


def find_articles_links(wiki_name: str, dump_date: str) -> dict:
    """Creates a list of article files to download.

    Args:
        base_url: The base URL the links are relative to.

    Returns:
        A list of file names to download.

    """
    dump_status_url = f'https://dumps.wikimedia.org/{wiki_name}/{dump_date}/dumpstatus.json'
    base_file_url = 'https://dumps.wikimedia.org/'

    page_text = request.urlopen(dump_status_url).read().decode('utf8')
    page = json.loads(page_text)
    files = page['jobs']['articlesdump']['files']

    all_links = {}
    for file, data in files.items():
        all_links[file] = urljoin(base_file_url, data['url'])

    return all_links


def remove_namespace(xml_string: str) -> ET.Element:
    """Removes namespace information from an XML document.

    Source: https://stackoverflow.com/a/25920989

    Args:
        xml_string: A string containing an XML document.

    Returns:
        The XML document without namespaces.

    """
    xml_iter = ET.iterparse(StringIO(xml_string))
    for _, element in xml_iter:
        if '}' in element.tag:
            element.tag = element.tag.split('}', 1)[1]  # Strip all namespaces
    root = xml_iter.root
    return root


def get_page_buffered(link: str) -> ET.Element:
    # Memory-saving trick found at http://enginerds.craftsy.com/blog/2014/04/parsing-large-xml-files-in-python-without-a-billion-gigs-of-ram.html
    input_buffer = ''
    with open(link, 'r', encoding='utf-8') as in_file:
        append = False
        for line in in_file:
            if '<page>' in line:
                input_buffer = line
                append = True
            elif '</page>' in line:
                input_buffer += line
                append = False
                page = remove_namespace(input_buffer)
                yield page
                input_buffer = None
            elif append:
                input_buffer += line


def get_page_parsed(link: str) -> ET.Element:
    xml_text = open(link, encoding='utf8').read()
    xml_root = remove_namespace(xml_text)
    for page in xml_root.iter('page'):
        yield page


def main():
    """Extracts the text of pages on Wikipedia."""
    parser = argparse.ArgumentParser(description='Extracts text of animal pages on Wikipedia.')
    parser.add_argument('wiki_name', help='')
    parser.add_argument('dump_date', help='')
    parser.add_argument('out_file_name', help='')
    parser.add_argument('-r', action='store_true',
                        help='Redownload and reextract all files', dest='redownload')
    parser.add_argument('-t', action='store_true',
                        help='Enable test mode, which processes only the first file', dest='test_mode')
    parser.add_argument('-s', action='store_true',
                        help='Skips downloading of .bz2 files', dest='skip_download')
    parser.add_argument('-b', action='store_true',
                        help='Loads XML file into a buffer instead of parsing entire file', dest='buffer_input')
    args = vars(parser.parse_args())
    wiki_name = args['wiki_name']
    dump_date = args['dump_date']
    out_file_name = args['out_file_name']
    redownload = args['redownload']
    test_mode = args['test_mode']
    skip_download = args['skip_download']
    buffer_input = args['buffer_input']

    articles_links = find_articles_links(wiki_name, dump_date)

    if not skip_download:
        for file_name, file_url in articles_links.items():
            if not os.path.isfile(file_name) or redownload:
                print(f'Downloading {file_name} now...')
                downloaded_file = request.urlopen(file_url).read()
                with bz2.open(file_name, 'w') as compressed_file:
                    compressed_file.write(downloaded_file)
            if test_mode:
                break
    for file_name in articles_links:
        if skip_download and not os.path.isfile(file_name):
            continue
        if not os.path.isfile(splitext(file_name)[0]) or redownload:
            print(f'Extracting {splitext(file_name)[0]} now...')
            with bz2.open(file_name, 'r') as compressed_file:
                compressed_file = compressed_file.read()
            decompressed_file = bz2.decompress(compressed_file).decode('utf8')
            with open(splitext(file_name)[0], 'w', encoding='utf8') as xml_file:
                xml_file.write(decompressed_file)
        if test_mode:
            break

    pages_saved = 0
    with open(out_file_name, 'w', encoding='utf-8') as out_file:
        for link in articles_links:
            if skip_download and not os.path.isfile(splitext(file_name)[0]):
                continue
            print(f'Processing {splitext(file_name)[0]} now...')

            if buffer_input:
                page_gen = get_page_buffered
            else:
                page_gen = get_page_parsed

            for page in page_gen(splitext(file_name)[0]):
                if page.find('ns').text == '0':
                    text = page.find('revision').find('text').text
                    text = wikicorpus.filter_wiki(text)
                    out_file.write(text + '\n\n')
                    pages_saved += 1

            if test_mode:
                break

    print(f'Stored {pages_saved} pages in {out_file_name}')


if __name__ == '__main__':
    main()
