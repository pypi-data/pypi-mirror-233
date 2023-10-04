from TurboTest.core.chemicals import Container
from TurboTest.error_tt import ErrorTT


def both_are_equal(x, y):
    Container.add_chemical()
    print('foooo')
    print(f"DEBUG: x: {repr(x)}  y: {repr(y)}")
    if x != y: raise ErrorTT('foo')
