from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


def this_is_True(condition:bool, /) -> None:
    """Guarantee the given `condition` is equal to `True`"""

    ## Metadata
    Container.add_chemical()

    ## Check
    if condition is False:
        raise ErrorTT('The given condition is `False`, expected `True`.')
