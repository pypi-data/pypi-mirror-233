

class ErrorTT(Exception):
    """custom exception for TT"""

    def __init__(self, message:str='', /) -> None:
        """
        ## Params
        - `message`: The message that will be printed if the test
                     fails (remember, yes, it's 'fail,' not 'error.'
                     Remember that tests fail and test error are two
                     different things).
        """
        super().__init__(message)
