from linguine.ops.StanfordCoreNLP import StanfordCoreNLP
from linguine.ops.bigram_array import BigramArray
from linguine.ops.char_ngrams import CharNgrams
from linguine.ops.lemmatize import LemmatizerWordNet
from linguine.ops.length_statistics import LengthStatistics
from linguine.ops.no_op import NoOp
from linguine.ops.remove_caps import RemoveCapsGreedy
from linguine.ops.remove_caps import RemoveCapsPreserveNNP
from linguine.ops.remove_hashtags import RemoveHashtags
from linguine.ops.remove_punct import RemovePunct
from linguine.ops.remove_quotes import RemoveQuotes
from linguine.ops.remove_silent_pauses import RemoveSilence
from linguine.ops.remove_stopwords import RemoveStopwords
from linguine.ops.sentence_tokenize import SentenceTokenize
from linguine.ops.splat import SplatComplexity, SplatDisfluency, SplatNGrams, SplatPOSFrequencies, SplatPronouns, \
    SplatSyllables
from linguine.ops.stem import StemmerPorter
from linguine.ops.tfidf import Tfidf
from linguine.ops.topic_model import TopicModel
from linguine.ops.unsupervised_morphology import UnsupervisedMorphology
from linguine.ops.word_cloud_op import WordCloudOp
from linguine.ops.word_tokenize import WordTokenizeStanford, WordTokenizeTreebank, WordTokenizeWhitespacePunct
from linguine.ops.word_vector import WordVector
from linguine.transaction_exception import TransactionException


def get_operation_handler(operation):
    if operation == 'lemmatize_wordnet':
        return LemmatizerWordNet()
    elif operation == 'removecapsgreedy':
        return RemoveCapsGreedy()
    elif operation == 'removecapsnnp':
        return RemoveCapsPreserveNNP()
    elif operation == 'removepunct':
        return RemovePunct()
    elif operation == 'removesilence':
        return RemoveSilence()
    elif operation == 'remove_stopwords':
        return RemoveStopwords()
    elif operation == 'sentence_tokenize':
        return SentenceTokenize()
    elif operation == 'removehashtags':
        return RemoveHashtags()
    elif operation == 'removequotes':
        return RemoveQuotes()
    elif operation == 'stem_porter':
        return StemmerPorter()
    elif operation == 'stop_words':
        return RemoveStopwords()
    elif operation == 'tfidf':
        return Tfidf()
    elif operation == 'wordcloudop':
        return WordCloudOp()
    elif operation == 'word_tokenize_treebank':
        return WordTokenizeTreebank()
    elif operation == 'word_tokenize_whitespace_punct':
        return WordTokenizeWhitespacePunct()
    elif operation == 'word_tokenize_stanford':
        return WordTokenizeStanford()
    elif operation == 'nlp-pos':
        return StanfordCoreNLP('pos')
    elif operation == 'nlp-ner':
        return StanfordCoreNLP('ner')
    elif operation == 'nlp-sentiment':
        return StanfordCoreNLP('sentiment')
    elif operation == 'nlp-coref':
        return StanfordCoreNLP('coref')
    elif operation == 'nlp-relation':
        return StanfordCoreNLP('relation')
    elif operation == 'splat-disfluency':
        print("YOU GOT SPLATTED")
        return SplatDisfluency()
    elif operation == 'splat-ngrams':
        print("YOU GOT SPLATTED")
        return SplatNGrams()
    elif operation == 'splat-complexity':
        print("YOU GOT SPLATTED")
        return SplatComplexity()
    elif operation == 'splat-pos':
        print("YOU GOT SPLATTED")
        return SplatPOSFrequencies()
    elif operation == 'splat-syllables':
        print("YOU GOT SPLATTED")
        return SplatSyllables()
    elif operation == 'splat-pronouns':
        print("YOU GOT SPLATTED")
        return SplatPronouns()
    elif operation == 'char-ngrams':
        return CharNgrams()
    elif operation == 'length-stats':
        return LengthStatistics()
    elif operation == 'topic-model-10':
        return TopicModel(10)
    elif operation == 'topic-model-30':
        return TopicModel(30)
    elif operation == 'word-vector':
        return WordVector()
    elif operation == 'unsup-morph':
        return UnsupervisedMorphology()
    elif operation == 'bigram-array':
        return BigramArray()
    elif operation == 'noop':
        return NoOp()
    else:
        raise TransactionException("The requested operation does not exist.")
