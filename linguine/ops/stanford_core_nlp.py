"""
Performs some CoreNLP operations as a proof of concept for the library.
"""

import json
import re

from stanfordcorenlp import StanfordCoreNLP as CoreNLP
from tatsu import parse


class StanfordCoreNLP:

    def __init__(self, analysis_type):
        self.analysis_type = analysis_type

        self.proc = CoreNLP('http://localhost', port=9000)
        self.props = {
            'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, sentiment, dcoref, relation, natlog, openie',
            'pipelineLanguage': 'en',
            'outputFormat': 'json',
            'timeout': 300_000  # 5 minutes in milliseconds
        }

    def run(self, data):
        result = self.json_cleanup(data, self.analysis_type)
        # print(result)
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
            res = self.proc.annotate(corpus.contents, properties=self.props)
            res = json.loads(res)
            # print(res)
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
                    # Add space after 'Very' for consistency and display
                    sentence['sentiment'] = sentence_res['sentiment'].replace('Very', 'Very ')

                    sentence['sentimentValue'] = int(sentence_res['sentimentValue'])
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
                    relations = []
                    predicates = dict()
                    for relation in sentence_res['openie']:
                        new_relation = {
                            'subject': {
                                'lemma': relation['subject'],
                                'start': relation['subjectSpan'][0],
                                'end': relation['subjectSpan'][1]
                            },
                            'relation': {
                                'lemma': relation['relation'],
                                'start': relation['relationSpan'][0],
                                'end': relation['relationSpan'][1]
                            },
                            'object': {
                                'lemma': relation['object'],
                                'start': relation['objectSpan'][0],
                                'end': relation['objectSpan'][1]
                            },
                        }
                        # Find the relation with longest arguments on left and right hand side
                        if relation['relation'] in predicates:
                            curr_relation = predicates[relation['relation']]
                            curr_length = (curr_relation['subject']['end'] - curr_relation['subject']['start']) + \
                                          (curr_relation['object']['end'] - curr_relation['object']['start'])

                            new_length = (new_relation['subject']['end'] - new_relation['subject']['start']) + \
                                         (new_relation['object']['end'] - new_relation['object']['start'])

                            if new_length > curr_length:
                                predicates[relation['relation']] = new_relation
                        else:
                            predicates[relation['relation']] = new_relation

                    for pred in predicates.values():
                        relations.append(pred)

                    sentence['relations'] = relations

                if analysis_type == 'pos':
                    sentence['tree_json'] = TreeStringToList.convert('parse', sentence_res['parse'])

                sentences.append(sentence)

        if analysis_type == 'coref':
            entities = []
            for entity_id, entity in res['corefs'].items():
                mentions = []
                for instance in entity:
                    mention = {
                        'mentionid': instance['id'],
                        'sentence': instance['sentNum'] - 1,
                        'tokspan_in_sentence': [
                            instance['startIndex'] - 1,
                            instance['endIndex'] - 1
                        ],
                        'head': instance['headIndex'] - 1,
                        'mentiontype': instance['type'],
                        'animacy': instance['animacy'],
                        'gender': instance['gender'],
                        'number': instance['number'],
                        'representative': instance['isRepresentativeMention']
                    }
                    mentions.append(mention)

                entities.append({'mentions': mentions, 'entityid': int(entity_id)})

            return {'sentences': sentences, 'entities': entities}
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

        nodes.append({'id': node_id, 'tag': '', 'head': head, 'value': ast['pos']})

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
