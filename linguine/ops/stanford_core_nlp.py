"""
Performs some CoreNLP operations as a proof of concept for the library.
"""

import json
import re

from stanfordcorenlp import StanfordCoreNLP as CoreNLP
from tatsu import parse


class StanfordCoreNLP:
    proc = None

    def __init__(self, analysis_type):
        self.analysis_type = analysis_type

        if StanfordCoreNLP.proc is None:
            StanfordCoreNLP.proc = CoreNLP('../stanford-corenlp-full-2018-10-05', quiet=False)
            StanfordCoreNLP.props = {
                'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, sentiment, dcoref, relation, natlog, openie',
                'pipelineLanguage': 'en',
                'outputFormat': 'json'
            }

    def run(self, data):
        result = self.json_cleanup(data, self.analysis_type)
        print(result)
        return result

    def json_cleanup(self, data, analysis_type):
        """
        When the JSON segments return from the CoreNLP library, they
        separate the data acquired from each word into their own element.

        For readability's sake, it would be nice to pair all of the information
        for a given word with that word, making a list of words with their
        part of speech tags
        """
        for corpus in data:
            res = StanfordCoreNLP.proc.annotate(corpus.contents, properties=StanfordCoreNLP.props)
            res = json.loads(res)
            print(res)
            sentences = []
            for sentence_res in res['sentences']:
                words = []
                for token in sentence_res['tokens']:
                    word = {'token': token['originalText']}

                    if analysis_type == 'ner':
                        word['ner'] = token['ner']

                    words.append(word)

                sentence = {'tokens': words}

                if analysis_type == 'sentiment':
                    sentence['sentiment'] = sentence_res['sentiment']
                    sentence['sentimentValue'] = sentence_res['sentimentValue']
                    sentence['tree_json'] = TreeStringToList.convert('sentiment', sentence_res['sentimentTree'])

                    # Extract sentiments from tree on a per-token level
                    value_to_name = {0: 'Very negative', 1: 'Negative', 2: 'Neutral', 3: 'Positive', 4: 'Very positive'}
                    sentiment_values = map(int, re.findall(r'\(\S+\|sentiment=(\d)\|prob=\d+\.\d+ \S+\)',
                                                           sentence_res['sentimentTree']))
                    for token, value in zip(words, sentiment_values):
                        token['sentiment'] = value_to_name[value]

                if analysis_type in ['sentiment', 'relation']:
                    sentence['parse'] = re.sub(r'\s+', ' ', sentence_res['parse'])

                if analysis_type == 'relation':
                    sentence['relations'] = sentence_res['openie']

                if analysis_type == 'pos':
                    sentence['tree_json'] = TreeStringToList.convert('parse', sentence_res['parse'])

                sentences.append(sentence)

        if analysis_type == 'coref':
            return {'sentences': sentences, 'entities': res['corefs']}
        else:
            return {'sentences': sentences}


class TreeStringToList:
    PARSE_GRAMMAR = r'''
        start = node $ ;
        node = '(' pos:tag value:children ')' | '(' pos:tag value:token ')' ;
        children = { node }+ ;
        tag = /\S+/ ;
        token = /\S+/ ;
    '''

    SENTIMENT_GRAMMAR = r'''
        start = node $ ;
        node = '(' tag:tag value:token ')' | '(' tag:tag value:children ')' ;
        children = { node }+ ;
        tag = pos:pos 'sentiment' sentiment:sentiment 'prob' prob ;
        pos = /\S+/ ;
        sentiment = /\d/ ;
        prob = /\d+\.\d+/ ;
        token = /\S+/ ;
    '''

    # Test with these
    # '(ROOT\n  (S\n    (NP (DT The) (JJ quick) (JJ brown) (NN fox))\n    (VP (VBD jumped)\n      (PP (IN over)\n        (NP (DT the) (JJ lazy) (NN dog))))\n    (. .)))'
    # '(ROOT|sentiment=1|prob=0.550\n  (NP|sentiment=2|prob=0.946 (DT|sentiment=2|prob=0.993 The)\n    (@NP|sentiment=2|prob=0.871 (JJ|sentiment=2|prob=0.993 quick)\n      (@NP|sentiment=2|prob=0.697 (JJ|sentiment=2|prob=0.929 brown) (NN|sentiment=2|prob=0.631 fox))))\n  (@S|sentiment=1|prob=0.510\n    (VP|sentiment=2|prob=0.469 (VBD|sentiment=2|prob=0.631 jumped)\n      (PP|sentiment=2|prob=0.620 (IN|sentiment=2|prob=0.991 over)\n        (NP|sentiment=2|prob=0.480 (DT|sentiment=2|prob=0.994 the)\n          (@NP|sentiment=1|prob=0.489 (JJ|sentiment=1|prob=0.716 lazy) (NN|sentiment=3|prob=0.852 dog)))))\n    (.|sentiment=2|prob=0.997 .)))'

    @staticmethod
    def convert(result_type, text):
        text = text.replace('(', ' ( ').replace(')', ' ) ')
        if result_type == 'parse':
            text = text[7:-2]
            ast = parse(TreeStringToList.PARSE_GRAMMAR, text)
            tree = TreeStringToList.flatten_parse_ast(ast)
        elif result_type == 'sentiment':
            text = text.replace('|', ' ').replace('=', ' ')
            ast = parse(TreeStringToList.SENTIMENT_GRAMMAR, text)
            tree = TreeStringToList.flatten_sentiment_ast(ast)
        else:
            raise NotImplementedError(f'Analysis type "{result_type}" not implemented')

        tree.sort(key=lambda x: x['id'])
        return tree

    @staticmethod
    def flatten_parse_ast(ast, nodes=None, head=None):
        if nodes is None:
            nodes = []
        if head is None:
            head = 0

        prev_ids = [node['id'] for node in nodes]
        node_id = max(prev_ids) + 1 if prev_ids else head + 1

        nodes.append({'id': node_id, 'tag': ast['pos'], 'head': head, 'value': ast['pos']})

        if isinstance(ast['value'], str):
            nodes.append({'id': node_id + 1, 'tag': '', 'head': node_id, 'value': ast['value']})
        elif isinstance(ast['value'], list):
            for child in ast['value']:
                TreeStringToList.flatten_parse_ast(child, nodes, node_id)
        else:
            raise RuntimeError(f'Unexpected type "{ast["value"]}"')

        return nodes

    @staticmethod
    def flatten_sentiment_ast(ast, nodes=None, head=None):
        if nodes is None:
            nodes = []
        if head is None:
            head = 0

        prev_ids = [node['id'] for node in nodes]
        node_id = max(prev_ids) + 1 if prev_ids else head + 1

        nodes.append({'id': node_id, 'tag': int(ast['tag']['sentiment']), 'head': head, 'value': ast['tag']['pos']})

        if isinstance(ast['value'], str):
            nodes.append({'id': node_id + 1, 'tag': '', 'head': node_id, 'value': ast['value']})
        elif isinstance(ast['value'], list):
            for child in ast['value']:
                TreeStringToList.flatten_sentiment_ast(child, nodes, node_id)
        else:
            raise RuntimeError(f'Unexpected type "{ast["value"]}"')

        return nodes
