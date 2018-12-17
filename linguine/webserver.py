"""
The Tornado server used to receive operation requests and deliver results to the user.
"""
import json
import os
import traceback
from concurrent.futures import ThreadPoolExecutor

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

    def post(self):
        self.set_header('Content-Type', 'application/json')
        try:
            self.num_transactions_running += 1
            transaction = Transaction()
            self.transactions.append(transaction)
            transaction.parse_json(self.request.body)
            transaction.read_corpora(transaction.corpora_ids)
            transaction.calcETA(self.num_transactions_running)
            analysis_id = transaction.create_analysis_record()

            # Generate response to server before kicking off analysis
            self.write(json.JSONEncoder().encode({'analysis_id': str(analysis_id)}))
            self.finish()

            # Encapsulate running of analysis in a future
            print("Submitting analysis " + str(analysis_id) + " to analysis queue")
            self.analysis_executor.submit(transaction.run, analysis_id, self)

            for p in psutil.pids():
                if psutil.Process(p).name() in ["python3.4", "java"]:
                    for child in psutil.Process(p).children():
                        cdict = child.as_dict(attrs=['pid', 'name', 'status', 'ppid'])
                        print("\t" + str(cdict))
                        if cdict['status'] in ['sleeping', 'zombie'] and self.num_transactions_running == 0:
                            print("There are no transactions running currently. Cleaning up idle java threads.")
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
            self.write(json.JSONEncoder().encode({'error': err}))


def main():
    try:
        application = tornado.web.Application([(r"/", MainHandler)])
        application.listen(5555)
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
