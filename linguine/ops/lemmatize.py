"""
Returns: A list of lemmas generated from the given corpora
Given: Tokenized contents of corpora
Uses the NLTK POS Tagger (Penn Treebank) to look up parts of speech,
and the WordNet Lemmatizer to get the lemma for each word.
"""
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer


class LemmatizerWordNet:
    def __init__(self):
        pass

    def run(self, data):
        for corpus in data:
            tags = pos_tag(corpus.tokenized_contents)
            lemmatizer = WordNetLemmatizer()
            corpus.tokenized_contents = [lemmatizer.lemmatize(word, self.get_word_net_part_of_speech(tag))
                                         if self.get_word_net_part_of_speech(tag) is not None
                                         else word
                                         for (word, tag) in tags]

            corpus.contents = ' '.join(corpus.tokenized_contents)

        return data

    def get_word_net_part_of_speech(self, treebank_tag):
        """
        So the WordNetLemmatizer in NLTK expects POS tags in a different format than NLTK itself writes them.
        So this function does the conversion to make them compatible.
        """
        if treebank_tag.startswith('J'):
            return 'a'
        elif treebank_tag.startswith('V'):
            return 'v'
        elif treebank_tag.startswith('N'):
            return 'n'
        elif treebank_tag.startswith('R'):
            return 'r'
