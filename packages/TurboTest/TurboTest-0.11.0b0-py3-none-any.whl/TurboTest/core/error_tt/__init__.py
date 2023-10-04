

class ErrorTT(Exception):
    """custom exception for TT"""

    def __init__(self, message):
        super().__init__(message)
