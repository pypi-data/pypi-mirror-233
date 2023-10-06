import re

from mykit.kit.readable.trim_long_str import trim_long_str

from TurboTest.constants import C
from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


def the_string_matches_the_regex(the_string:str, the_regex:str) -> None:
    r"""
    Guarantee that `the_string` matches `the_regex`

    ## Examples
    >>> the_string_matches_the_regex('1.2.3', r'^\d+\.\d+\.\d+$')

    ## Docs
    - This works fine for simple regex. For complex regex that use flags,
        multiline, etc., I'm not sure it can handle that yet. TODO: support these soon.
    - This func has minimal arg validations. Please input appropriate values that this func might expect.
    """

    ## Metadata
    Container.add_chemical()

    ## Check
    if not re.match(the_regex, the_string):
        
        ## Guard
        str_report = trim_long_str(repr(the_string), C.REPORT_LEN)

        ## Report
        raise ErrorTT(
            f"Oopsie! `the_string` does not match this regex {repr(the_regex)}.\n"
            f"  the_string: {str_report}"
        )
