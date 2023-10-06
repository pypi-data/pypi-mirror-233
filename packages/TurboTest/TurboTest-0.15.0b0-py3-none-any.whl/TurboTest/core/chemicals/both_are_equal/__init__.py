from typing import Any

# from ...chemicals import Container
# from ....core.error_tt import ErrorTT
## vvvvvvvvvvvvvvvv dev-docs: using relative imports is concise (saves disk) but so unreadable
from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


def both_are_equal(X:Any, Y:Any, /) -> None:
    """Guarantee that `X == Y` must be true."""
    
    ## Metadata
    Container.add_chemical()
    
    ## Check
    if X != Y:
        raise ErrorTT(
            f"X should be equal to Y, but they aren't.\n"
            f"  X: {repr(X)}\n"
            f"  Y: {repr(Y)}"
        )
