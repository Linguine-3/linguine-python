import json
import time
import traceback

from bson.errors import InvalidId
from bson.objectid import ObjectId

import linguine.operation_builder
from linguine.corpus import Corpus
from linguine.database_adapter import DatabaseAdapter
from linguine.transaction_exception import TransactionException


class Transaction:
    def __init__(self):
        self.transaction_id = -1
        self.eta = None
        self.library = None
        self.operation = None
        self.user_id = None
        self.corpora_ids = []
        self.time_created = None
        self.corpora = []
        self.analysis_name = ""
        self.cleanups = []
        self.current_result = None
        self.tokenizer = None
        self.token_based_operations = ['tfidf', 'word_cloud_op',
                                       'stem_porter', 'stem_lancaster',
                                       'stem_snowball', 'lemmatize_wordnet']
        self.is_finished = False

    def read_corpora(self):
        """Read in all corpora that are specified for a given transaction"""
        try:
            # load corpora from database
            corpora = DatabaseAdapter.get_db().corpus
            for corpus_id in self.corpora_ids:
                corpus = corpora.find_one({"_id": ObjectId(corpus_id)})
                self.corpora.append(Corpus(corpus_id, corpus["title"],
                                           corpus["contents"], corpus["tags"]))
        except (TypeError, InvalidId):
            raise TransactionException('Could not find corpus.')

    def create_analysis_record(self):
        """
        Insert an analysis record into the database,
        acknowledging that an analysis is to be processed.
        """
        analysis = {'user_id': ObjectId(self.user_id),
                    'analysis_name': self.analysis_name,
                    'corpora_ids': self.corpora_ids,
                    'cleanup_ids': self.cleanups,
                    'result': "",
                    'tokenizer': self.tokenizer,
                    'eta': self.eta,
                    'complete': False,
                    'time_created': self.time_created,
                    'analysis': self.operation}
        return DatabaseAdapter.get_db().analyses.insert_one(analysis).inserted_id

    def write_result(self, result, analysis_id):
        """Write result object to DB"""
        analysis = DatabaseAdapter.get_db().analyses.find_one({"_id": ObjectId(analysis_id)})

        analysis['complete'] = True
        analysis['result'] = result

        print("Analysis " + str(analysis_id) + " complete. submitting record to DB")

        DatabaseAdapter.get_db().analyses.update_one({'_id': ObjectId(analysis_id)}, {'$set': analysis})
        self.is_finished = True

    def parse_json(self, json_data):
        """
        Parse a JSON request from the linguine-node webserver,
        Requesting that an analysis should be preformed
        """
        try:
            input_data = json.loads(json_data.decode())

            self.transaction_id = input_data['transaction_id']
            self.operation = input_data['operation']
            self.library = input_data['library']
            self.analysis_name = input_data['analysis_name']
            self.time_created = input_data['time_created']

            if 'user_id' in input_data.keys():
                self.user_id = input_data['user_id']
            if 'cleanup' in input_data.keys():
                self.cleanups = input_data['cleanup']
            self.corpora_ids = input_data['corpora_ids']
            if 'tokenizer' in input_data.keys():
                self.tokenizer = input_data['tokenizer']

        except KeyError:
            raise TransactionException('Missing property transaction_id, operation, library, tokenizer or corpora_ids.')
        except ValueError:
            raise TransactionException('Could not parse JSON.')

    def calc_eta(self, num_transactions):
        """
        Calculate the estimated time that a transaction will require to complete.
        this will be stored in the database record to display on the client
        """
        time_est = 0
        # For now, assume the transaction queue adds 30secs per transaction
        time_est += num_transactions * 30
        # Check which type of transaction is being preformed
        if "nlp" in self.operation:
            # A raw guess that a CoreNLP analysis will take 1 second per
            # 10 words processed.
            time_est += (len(self.corpora[0].contents.split(" ")) / 10)

        self.eta = time_est

    def run(self, analysis_id, main_handler):
        """
        Execute the given analysis that has been fetched from the thread pool
        @args: MainHandler - Instance of parent class that keeps track of
        num of Transactions
               analysis_id - unique identifier of this Transaction
        """
        try:
            start = time.process_time()
            corpora = self.corpora
            if self.tokenizer is not None and not self.tokenizer == '':
                op_handler = linguine.operation_builder \
                    .get_operation_handler(self.tokenizer)
                op_handler.run(corpora)
            for cleanup in self.cleanups:

                op_handler = linguine.operation_builder. \
                    get_operation_handler(cleanup)
                corpora = op_handler.run(corpora)
                # Corpora must be re tokenized after each cleanup
                if self.tokenizer is not None and not self.tokenizer == '':
                    op_handler = linguine.operation_builder \
                        .get_operation_handler(self.tokenizer)
                    op_handler.run(corpora)

            op_handler = linguine.operation_builder. \
                get_operation_handler(self.operation)

            print("Performing core operation for analysis " + str(analysis_id) + " with op " + str(op_handler))
            self.write_result(op_handler.run(corpora), str(analysis_id))

            # write transaction time to console
            print(self.analysis_name, ',', (time.process_time() - start) * 1000)
            # Subtract one from analysis running count now that we're complete
            main_handler.num_transactions_running -= 1

        except Exception as e:
            # print(e.error)
            print("===========error==================")
            print(e)
            print(e.args)
            traceback.print_exc()
            # print(json.JSONEncoder().encode({'error': e.error}))
            print("===========end_error==================")
