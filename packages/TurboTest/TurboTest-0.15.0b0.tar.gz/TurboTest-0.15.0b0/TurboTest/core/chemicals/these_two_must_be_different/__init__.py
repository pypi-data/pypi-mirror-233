from typing import Any

from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


def these_two_must_be_different(X:Any, Y:Any, /) -> None:
    """Guarantee that `X != Y` must be true."""

    ## Metadata
    Container.add_chemical()

    ## Check
    if X == Y:
        raise ErrorTT(
            f"X and Y should be different, but they are the same.\n"
            f"  X: {repr(X)}\n"
            f"  Y: {repr(Y)}"
        )
