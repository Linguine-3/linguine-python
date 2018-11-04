"""
Author: Alex Hedges
"""

import argparse
import bz2
import os
import re
import xml.etree.ElementTree as ET
from io import StringIO
from os.path import basename
from os.path import splitext
from urllib import request
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from gensim.corpora import wikicorpus


def find_articles_links(base_url: str) -> list:
    """Creates a list of article files to download.

    Args:
        base_url: The base URL the links are relative to.

    Returns:
        A list of file names to download.

    """
    html = request.urlopen(base_url).read().decode('utf8')  # Download HTML
    soup = BeautifulSoup(html, 'lxml')  # Parse HTML
    all_links = []
    for link in soup.find_all('a'):
        all_links.append(link.get('href'))
    file_regex = re.compile(r'^vowiki-latest-pages-articles\.xml\.bz2$')
    articles_links = [link for link in all_links if file_regex.match(link)]
    return articles_links


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
    with open(link + '.xml', 'r') as in_file:
        append = False
        for line in in_file:
            if '<page>' in line:
                input_buffer = line
                append = True
            elif '</page>' in line:
                input_buffer += line
                append = False
                # print(input_buffer)
                page = remove_namespace(input_buffer)
                yield page
                input_buffer = None
                del input_buffer  # Probably redundant
            elif append:
                input_buffer += line


def get_page_parsed(link: str) -> ET.Element:
    xml_text = open(link + '.xml', encoding='utf8').read()
    xml_root = remove_namespace(xml_text)
    for page in xml_root.iter('page'):
        yield page


def main():
    """Extracts the text of pages on Wikipedia."""
    parser = argparse.ArgumentParser(description='Extracts text of animal pages on Wikipedia.')
    parser.add_argument('-r', action='store_true',
                        help='Redownload and reextract all files', dest='redownload')
    parser.add_argument('-t', action='store_true',
                        help='Enable test mode, which processes only the first file', dest='test_mode')
    parser.add_argument('-s', action='store_true',
                        help='Skips downloading of .bz2 files', dest='skip_download')
    parser.add_argument('-b', action='store_true',
                        help='Loads XML file into a buffer instead of parsing entire file', dest='buffer_input')
    args = vars(parser.parse_args())
    redownload = args['redownload']
    test_mode = args['test_mode']
    skip_download = args['skip_download']
    buffer_input = args['buffer_input']
    base_url = 'https://dumps.wikimedia.org/vowiki/latest/'
    articles_links = find_articles_links(base_url)
    articles_links = [splitext(basename(link))[0] for link in articles_links]
    if not skip_download:
        for link in articles_links:
            if not os.path.isfile(link + '.bz2') or redownload:
                print('Downloading {} now...'.format(link + '.bz2'), flush=True)
                downloaded_file = request.urlopen(urljoin(base_url, link + '.bz2')).read()
                with bz2.open(link + '.bz2', 'w') as compressed_file:
                    compressed_file.write(downloaded_file)
            if test_mode:
                break
    for link in articles_links:
        if skip_download and not os.path.isfile(link + '.bz2'):
            continue
        if not os.path.isfile(link + '.xml') or redownload:
            print('Extracting {} now...'.format(link + '.xml'), flush=True)
            with bz2.open(link + '.bz2', 'r') as compressed_file:
                compressed_file = compressed_file.read()
            decompressed_file = bz2.decompress(compressed_file).decode('utf8')
            with open(link + '.xml', 'w', encoding='utf8') as xml_file:
                xml_file.write(decompressed_file)
        if test_mode:
            break
    out_file_name = 'vowiki.txt'
    pages_saved = 0
    with open(out_file_name, 'w') as out_file:
        for link in articles_links:
            if skip_download and not os.path.isfile(link + '.xml'):
                continue
            print('Processing {} now...'.format(link + '.xml'), flush=True)

            if buffer_input:
                page_gen = get_page_buffered
            else:
                page_gen = get_page_parsed

            for page in page_gen(link):
                if page.find('ns').text == '0':
                    text = page.find('revision').find('text').text
                    text = wikicorpus.filter_wiki(text)
                    out_file.write(text + '\n\n')
                    pages_saved += 1

            if test_mode:
                break

    print('Stored {} pages in {}'.format(pages_saved, out_file_name))


if __name__ == '__main__':
    main()
