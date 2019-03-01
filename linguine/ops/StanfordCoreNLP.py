"""
Performs some CoreNLP operations as a proof of concept for the library.
"""

import json
import os

from stanford_corenlp_pywrapper import CoreNLP


class StanfordCoreNLP:
    proc = None

    def __init__(self, analysis_type):
        self.analysis_type = analysis_type

        # print("ANALYSIS: " + str(analysisType))

        if StanfordCoreNLP.proc is None:
            StanfordCoreNLP.proc = CoreNLP(configdict={
                'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, sentiment, dcoref, relation, natlog, openie'},
                corenlp_jars=[os.path.join(os.path.dirname(__file__),
                                           '../../../stanford_corenlp_pywrapper/stanford_corenlp_pywrapper/lib/*')])

    def run(self, data):
        result = self.json_cleanup(data, self.type_to_annotator(self.analysis_type))
        # print(result)
        return result

    def type_to_annotator(self, analysis_type):
        if analysis_type == 'pos':
            return ['pos']
        elif analysis_type == 'ner':
            return ['ner']
        elif analysis_type == 'sentiment':
            return ['parse', 'sentiment']
        elif analysis_type == 'coref':
            return ['tokenize', 'ssplit', 'coref']
        elif analysis_type == 'relation':
            return ['parse', 'relation']
        else:
            return None

    def json_cleanup(self, data, analysis_types):
        """
        When the JSON segments return from the CoreNLP library, they
        separate the data acquired from each word into their own element.

        For readability's sake, it would be nice to pair all of the information
        for a given word with that word, making a list of words with their
        part of speech tags
        """
        for corpus in data:
            res = StanfordCoreNLP.proc.parse_doc(corpus.contents)
            # print(res)
            sentences = []
            for sentence_res in res["sentences"]:
                words = []
                for index, token in enumerate(sentence_res["tokens"]):
                    word = {"token": sentence_res["tokens"][index]}
                    if 'coref' not in analysis_types:
                        for atype in analysis_types:
                            if atype is "sentiment":
                                word[atype] = sentence_res[atype]
                                word["sentimentValue"] = sentence_res["sentimentValue"]
                            elif atype is not "parse" and atype is not "relation":
                                word[atype] = sentence_res[atype][index]

                    words.append(word)
                sentence = {'tokens': words}
                if "sentiment" in analysis_types:
                    sentence['sentiment'] = sentence_res['sentiment']
                    sentence['sentimentValue'] = sentence_res['sentimentValue']
                    sentence['tree_json'] = json.loads(sentence_res['sentiment_json'])

                if "parse" in analysis_types:
                    sentence["parse"] = sentence_res["parse"]

                if "relation" in analysis_types:
                    sentence['relations'] = json.loads(sentence_res['relations'])

                if 'pos' in analysis_types:
                    sentence['tree_json'] = json.loads(sentence_res['deps_json'])

                sentences.append(sentence)

        if self.analysis_type == 'pos':
            for sentence in sentences:
                sentence['tokens'] = [{'token': token['token']} for token in sentence['tokens']]
            return {'sentences': sentences}
        elif self.analysis_type in ['ner', 'sentiment']:
            return {'sentences': sentences}
        else:
            return {"sentences": sentences, "entities": res["entities"]}
