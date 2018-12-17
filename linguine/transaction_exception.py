class TransactionException(Exception):
    def __init__(self, error_message, code=400):
        # Set some exception information
        self.error = error_message
        self.code = code
