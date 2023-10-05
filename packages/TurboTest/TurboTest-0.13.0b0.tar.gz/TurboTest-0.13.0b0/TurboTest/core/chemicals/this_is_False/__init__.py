from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


def this_is_False(condition:bool, /) -> None:
    """Guarantee the given `condition` is equal to `False`"""

    ## Metadata
    Container.add_chemical()

    ## Check
    if condition is True:
        raise ErrorTT('Expected False, but the given condition evaluated to True.')
