"""
Returns:
Given:
"""

import json
import re

import splat.Util as Util
import splat.complexity as cUtil
from splat.SPLAT import SPLAT
from splat.parsers.TreeStringParser import TreeStringParser

from linguine.transaction_exception import TransactionException


class SplatDisfluency:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        try:
            for corpus in data:
                temp_bubble = SPLAT(corpus.contents)
                print(corpus.contents)
                print(temp_bubble.sents())
                raw_disfluencies = Util.count_disfluencies(temp_bubble.sents())
                print(raw_disfluencies)
                sentences = {}
                average_disfluencies = 0
                um_count, uh_count, ah_count, er_count, hm_count, sl_count, rep_count, brk_count = (0,) * 8
                # Sort the data so it looks better in JSON
                for i in raw_disfluencies[0]:
                    temp_dis = {"UM": raw_disfluencies[0][i][0], "UH": raw_disfluencies[0][i][1],
                                "AH": raw_disfluencies[0][i][2],
                                "ER": raw_disfluencies[0][i][3], "HM": raw_disfluencies[0][i][4],
                                "SILENT PAUSE": raw_disfluencies[0][i][5],
                                "REPETITION": raw_disfluencies[0][i][6], "BREAK": raw_disfluencies[0][i][7]}
                    sentences[i] = temp_dis
                    for (k, v) in temp_dis.items():
                        # Gather total disfluencies for each disfluency type
                        average_disfluencies += v
                        if k == "UM":
                            um_count += v
                        elif k == "UH":
                            uh_count += v
                        elif k == "AH":
                            ah_count += v
                        elif k == "ER":
                            er_count += v
                        elif k == "HM":
                            hm_count += v
                        elif k == "SILENT PAUSE":
                            sl_count += v
                        elif k == "REPETITION":
                            rep_count += v
                        elif k == "BREAK":
                            brk_count += v

                temp_total = average_disfluencies

                # Calculate the average disfluencies per sentence in the whole text
                average_disfluencies = float(average_disfluencies / len(raw_disfluencies[0]))

                total_disfluencies = {"UM": um_count, "UH": uh_count, "AH": ah_count, "ER": er_count, "HM": hm_count,
                                      "SILENT PAUSE": sl_count, "REPETITION": rep_count, "BREAK": brk_count,
                                      "TOTAL": temp_total}

                results.append({'corpus_id': corpus.id,
                                'sentences': sentences,
                                'average_disfluencies_per_sentence': average_disfluencies,
                                'total_disfluencies': total_disfluencies})
            results = json.dumps(results)
            print(results)
            return results
        except TypeError:
            raise TransactionException('Corpus contents does not exist.')


class SplatNGrams:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        try:
            for corpus in data:
                temp_bubble = SPLAT(corpus.contents)
                # Gather Unigram Frequencies
                temp_unigrams = temp_bubble.unigrams()
                unigrams = dict()
                for item in temp_unigrams:
                    unigrams[item[0]] = unigrams.get(item[0], 0) + 1

                # Gather Bigram Frequencies
                temp_bigrams = temp_bubble.bigrams()
                bigrams = dict()
                for item in temp_bigrams:
                    parsed_item = ' '.join(item)
                    bigrams[parsed_item] = bigrams.get(parsed_item, 0) + 1

                # Gather Trigram Frequencies
                temp_trigrams = temp_bubble.trigrams()
                trigrams = dict()
                for item in temp_trigrams:
                    parsed_item = ' '.join(item)
                    trigrams[parsed_item] = trigrams.get(parsed_item, 0) + 1

                results.append({'corpus_id': corpus.id,
                                'unigrams': unigrams,
                                'bigrams': bigrams,
                                'trigrams': trigrams})
            results = json.dumps(results)
            # print(results)
            return results
        except TypeError:
            raise TransactionException('Corpus contents does not exist.')


class SplatComplexity:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        try:
            for corpus in data:
                split_string = corpus.contents.split(" ")
                temp_corpus = list(filter("{SL}".__ne__, split_string))
                temp_corpus = list(filter("{sl}".__ne__, temp_corpus))
                temp_corpus_contents = " ".join(temp_corpus)
                # print(corpus.contents)
                temp_bubble = SPLAT(temp_corpus_contents)
                temp_trees = TreeStringParser().get_parse_trees(temp_bubble.sents())
                # print(temp_bubble.splat())
                # cdensity = temp_bubble.content_density()
                cdensity = cUtil.calc_content_density(temp_trees)
                print(cdensity)
                # print(temp_bubble.treestrings())
                # idensity = temp_bubble.idea_density()
                idensity = cUtil.calc_idea_density(temp_trees)[0]
                # print(idensity)
                flesch_score = temp_bubble.flesch_readability()
                # print(flesch_score)
                kincaid_score = temp_bubble.kincaid_grade_level()
                # print(kincaid_score)
                types = len(temp_bubble.types())
                tokens = len(temp_bubble.tokens())
                type_token_ratio = float(float(types) / float(tokens))
                results.append({'corpus_id': corpus.id,
                                'content_density': cdensity,
                                'idea_density': idensity,
                                'flesch_score': flesch_score,
                                'kincaid_score': kincaid_score,
                                'types': types,
                                'tokens': tokens,
                                'type_token_ratio': type_token_ratio})
            results = json.dumps(results)
            # print(results)
            return results
        except TypeError as e:
            print(e)
            raise TransactionException('Corpus contents does not exist.')
        # except Exception as e:
        #    print(e)
        #    traceback.print_stack()


class SplatPOSFrequencies:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        pos_parsed = {}
        try:
            for corpus in data:
                temp_bubble = SPLAT(corpus.contents)
                pos_tags = temp_bubble.pos()
                pos_counts = temp_bubble.pos_counts()
                for k, v in pos_tags:
                    if v in pos_parsed.keys():
                        if k not in pos_parsed[v]:
                            pos_parsed[v].append(k)
                    else:
                        pos_parsed[v] = []
                        pos_parsed[v].append(k)

                results.append({'corpus_id': corpus.id,
                                'pos_tags': pos_parsed,
                                'pos_counts': pos_counts})

            results = json.dumps(results)
            print(results)
            return results
        except TypeError as e:
            print(e)
            raise TransactionException('Failed to run SplatPOSFrequencies.')


class SplatSyllables:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        syllables_parsed = {}
        try:
            for corpus in data:
                # temp_bubble = SPLAT(corpus.contents)
                split_string = re.split(r'\s|\n', corpus.contents)
                temp_corpus = list(filter("{SL}".__ne__, split_string))
                temp_corpus = list(filter("{sl}".__ne__, temp_corpus))
                temp_corpus_contents = " ".join(temp_corpus)
                temp_bubble = SPLAT(temp_corpus_contents.rstrip('\n'))
                temp_tokens = temp_bubble.tokens()
                temp_tokens = ' '.join(temp_tokens).strip("\n").split(' ')
                print(temp_tokens)
                for tok in temp_tokens:
                    temp_tok = tok.strip("\n")
                    temp_syll_count = cUtil.num_syllables([temp_tok])
                    if temp_syll_count == 0:
                        temp_syll_count = 1
                    if str(temp_syll_count) in syllables_parsed.keys():
                        if tok not in syllables_parsed[str(temp_syll_count)]:
                            syllables_parsed[str(temp_syll_count)].append(temp_tok)
                    else:
                        syllables_parsed[str(temp_syll_count)] = []
                        syllables_parsed[str(temp_syll_count)].append(temp_tok)

                print("Creating results...")
                results.append({'corpus_id': corpus.id,
                                'syllables': syllables_parsed})

            results = json.dumps(results)
            print(results)
            return results
        except TypeError as e:
            print(e)
            raise TransactionException('Failed to run SplatSyllables.')


class SplatPronouns:
    def __init__(self):
        pass

    def run(self, data):
        results = []
        first = {}
        second = {}
        third = {}
        try:
            for corpus in data:
                temp_corpus = " ".join(re.split(r'\s|\n', corpus.contents))
                temp_bubble = SPLAT(temp_corpus.rstrip("\n"))
                pronouns = temp_bubble.raw_pronouns()
                print(pronouns)
                sents = temp_bubble.sents()

            for p, v in pronouns.items():
                if v[1] == "1st-Person":
                    first[p] = v
                elif v[1] == "2nd-Person":
                    second[p] = v
                elif v[1] == "3rd-Person":
                    third[p] = v

            results.append({'corpus_id': corpus.id,
                            'first-person': first,
                            'second-person': second,
                            'third-person': third,
                            'sentences': sents})

            results = json.dumps(results)
            print(results)
            return results
        except TypeError as e:
            print(e)
            raise TransactionException("Failed to run SplatPronouns.")
