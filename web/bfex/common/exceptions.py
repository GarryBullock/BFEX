class DataIngestionException(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)

        # If we decide to implement logging in the future, this will be useful for tracking errors.
        self.code = code
