from mykit.kit.misc.get_py_ver import get_py_ver
from mykit.kit.time import TimeFmt

from TurboTest.constants import __version__


def print_header(cwd):
    
    header = f'TurboTest-{__version__} 🐍{get_py_ver()}  at {repr(cwd)}  « {TimeFmt.full()} »'
    print(header)
