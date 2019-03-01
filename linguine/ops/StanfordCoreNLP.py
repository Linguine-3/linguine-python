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

        if StanfordCoreNLP.proc is None:
            StanfordCoreNLP.proc = CoreNLP(configdict={
                'annotators': 'tokenize, ssplit, pos, lemma, ner, parse, sentiment, dcoref, relation, natlog, openie'},
                corenlp_jars=[os.path.join(os.path.dirname(__file__),
                                           '../../../stanford_corenlp_pywrapper/stanford_corenlp_pywrapper/lib/*')])

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
            res = StanfordCoreNLP.proc.parse_doc(corpus.contents)
            # print(res)
            sentences = []
            for sentence_res in res["sentences"]:
                words = []
                for index, token in enumerate(sentence_res["tokens"]):
                    word = {"token": token}

                    if analysis_type == "sentiment":
                        word['sentiment'] = sentence_res['sentiments'][index]
                    elif analysis_type == 'ner':
                        word['ner'] = sentence_res['ner'][index]

                    words.append(word)

                sentence = {'tokens': words}

                if analysis_type == "sentiment":
                    sentence['sentiment'] = sentence_res['sentiment']
                    sentence['sentimentValue'] = sentence_res['sentimentValue']
                    sentence['tree_json'] = json.loads(sentence_res['sentiment_json'])

                if analysis_type in ['sentiment', 'relation']:
                    sentence["parse"] = sentence_res["parse"]

                if analysis_type == "relation":
                    sentence['relations'] = json.loads(sentence_res['relations'])

                if analysis_type == 'pos':
                    sentence['tree_json'] = json.loads(sentence_res['deps_json'])

                sentences.append(sentence)

        if analysis_type == 'coref':
            return {'sentences': sentences, "entities": res["entities"]}
        else:
            return {"sentences": sentences}
