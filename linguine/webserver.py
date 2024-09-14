"""
The Tornado server used to receive operation requests and deliver results to the user.
"""
import json
import os
import traceback
from concurrent.futures import ThreadPoolExecutor

import argparse
import psutil
import tornado.ioloop
import tornado.web

from linguine.transaction import Transaction
from linguine.transaction_exception import TransactionException


class MainHandler(tornado.web.RequestHandler):
    num_transactions_running = 0
    transactions = []
    try:
        max_thread_pool_workers = int(os.environ['LINGUINE_THREADS'])
    except KeyError:
        max_thread_pool_workers = 2
    print("starting thread pool with " + str(max_thread_pool_workers) + " threads.")
    analysis_executor = ThreadPoolExecutor(max_workers=max_thread_pool_workers)

    def initialize(self, database):
        self.database = database

    def post(self):
        self.set_header('Content-Type', 'application/json')
        try:
            self.num_transactions_running += 1
            transaction = Transaction(self.database)
            self.transactions.append(transaction)
            transaction.parse_json(self.request.body)
            transaction.read_corpora()
            transaction.calc_eta(self.num_transactions_running)
            analysis_id = transaction.create_analysis_record()

            # Generate response to server before kicking off analysis
            self.write(json.JSONEncoder().encode({'analysis_id': str(analysis_id)}))
            self.finish()

            # Encapsulate running of analysis in a future
            print("Submitting analysis " + str(analysis_id) + " to analysis queue")
            self.analysis_executor.submit(transaction.run, analysis_id, self)

            for p in psutil.pids():
                if psutil.Process(p).name() in ["python", "java"]:
                    for child in psutil.Process(p).children():
                        cdict = child.as_dict(attrs=['pid', 'name', 'status', 'ppid'])
                        print("\t" + str(cdict))
                        if cdict['status'] in ['sleeping', 'zombie'] and self.num_transactions_running == 0:
                            print("There are no transactions running currently. Cleaning up idle threads.")
                            child.kill()

        except TransactionException as err:
            print("===========error==================")
            print(err.error)
            try:
                print(json.JSONEncoder().encode({'error': err.error}))
            except AttributeError as e:
                print(json.JSONEncoder().encode({'error': e}))
            print("===========end_error==================")
            self.set_status(err.code)
            self.write(json.JSONEncoder().encode({'error': err.error}))

        # Keep this error instance as a catch-all for all web requests
        except Exception as err:
            print("===========error==================")
            print(err)
            print(err.args)
            traceback.print_exc()
            print("===========end_error==================")


def main():
    if 'NODE_ENV' in os.environ:
        # Look for Node environment to determine db name.
        db = 'linguine2' + os.environ['NODE_ENV']
    else:
        # NODE_ENV not found, default to development
        db = 'linguine2-development'

    parser = argparse.ArgumentParser()

    # Defaults are set for Linguine 1
    parser.add_argument("--port", type=int, default=5551)
    parser.add_argument("--database", type=str, default=db)
    args = parser.parse_args()

    print(f"Using database: {args.database}")
    print(f"Starting server on {args.port}")
    try:
        application = tornado.web.Application([(r"/", MainHandler, dict(database=args.database))])
        application.listen(args.port)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
    # Keep this error instance as a catch-all for all web requests
    except Exception as err:
        print("===========error==================")
        print(err)
        print(err.args)
        traceback.print_exc()
        print("===========end_error==================")


if __name__ == "__main__":
    main()
