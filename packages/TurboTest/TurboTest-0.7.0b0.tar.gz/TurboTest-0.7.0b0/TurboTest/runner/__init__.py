import os
import time

from mykit.kit.color import Hex, Colored
from mykit.kit.time import TimeFmt
from mykit.kit.readable.make_separator import make_separator
from mykit.kit.readable.time_quick import time_quick
from mykit.ghactions.eLog import eL


class C:  # Constants

    T0 = time.time()
    CWD = os.getcwd()


class R:  # Runtime

    nPass = 0
    nFail = 0
    t_core = 0  # in seconds

    details = []


def run():

    ## Debugging purposes
    eL.debug(os.listdir(C.CWD))


    SEP = make_separator('─', 140)

    ## Header
    print(f'TurboTest... at {repr(C.CWD)}  ({TimeFmt.full()})')
    print(SEP)

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
