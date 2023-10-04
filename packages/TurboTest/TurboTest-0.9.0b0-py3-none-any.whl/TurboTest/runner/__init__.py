import os, re
import time

from mykit.kit.color import Hex, Colored
from mykit.kit.time import TimeFmt
from mykit.kit.readable.make_separator import make_separator
from mykit.kit.readable.time_quick import time_quick
from mykit.ghactions.eLog import eL
from mykit.kit.fileops.simple import list_dir
from mykit.kit.fileops.nice_io import NiceIO


class C:  # Constants

    T0 = time.time()
    CWD = os.getcwd()


class R:  # Runtime

    nPass = 0
    nFail = 0
    t_core = 0  # in seconds

    details = []


def recur(dir_pth):
    
    for name, pth in list_dir(dir_pth):
        if os.path.isdir(pth):
            recur(pth)
        else:
            if name == 'test.py':
                content = NiceIO.read(pth)
                if content.startswith('import TurboTest as tt'):
                    funcs = []
                    for line in content.split('\n'):
                        res = re.match(r'^def (?P<name>\w+)\(.+', line)
                        if res is not None:
                            f = res.group('name')
                            if not f.startswith('_'):
                                funcs.append(f)
                    print(f'funcs={funcs}  at {repr(pth)}')

def run_tests(cwd):
    
    recur(cwd)


def run():

    ## Debugging purposes
    eL.debug(os.listdir(C.CWD))


    SEP = make_separator('─', length_backup=110)

    ## Header
    print(f'TurboTest... at {repr(C.CWD)}  ({TimeFmt.full()})')
    print(SEP)

    run_tests(C.CWD)

    body = 'okay123'
    print(body)

    nTest = R.nPass + R.nFail

    T_CORE = time_quick(R.t_core)
    T_TOTAL = time_quick(time.time() - C.T0)

    footer = (
        f'Done, {nTest} test functions '
        f'[pass/fail: {R.nPass}/{R.nFail}] '
         'executed in '
        f'[core/total: {T_CORE}/{T_TOTAL}] 🔥🔥'
    )
    print(SEP)
    print(footer)
