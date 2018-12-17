"""
Removes all non-proper-noun capitals from a given text.
Removes capital letters from text, even for Bill Clinton.
Accepts as input a non-tokenized string.
There are multiple types of cap-removal to do.
greedy: removes all caps. GOAL -> goal, Mr. -> mr., Cook -> cook
preserve_nnp: removes capitalization that isn't a proper noun.
"""
from textblob import TextBlob


class RemoveCapsGreedy:
    def run(self, data):
        results = []
        for corpus in data:
            corpus.contents = corpus.contents.lower()
            results.append(corpus)
        return results


class RemoveCapsPreserveNNP:
    def run(self, data):
        results = []
        for corpus in data:
            blob = TextBlob(corpus.contents)
            tags = blob.tags
            words = list()
            word_count = 0
            token_count = 0
            while token_count < len(blob.tokens):
                if blob.tokens[token_count][0].isalpha():
                    if tags[word_count][1] != 'NNP':
                        words.append(blob.words[word_count].lower())
                    else:
                        words.append(blob.words[word_count])
                    word_count += 1
                else:
                    words[len(words) - 1] = ''.join(
                        [words[len(words) - 1], blob.tokens[token_count]])
                token_count += 1
            corpus.contents = (' '.join(words))
            results.append(corpus)
        return results
