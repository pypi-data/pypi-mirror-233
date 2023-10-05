import os, re, sys
import time

from mykit.kit.color import Hex, Colored
from mykit.kit.time import TimeFmt
from mykit.kit.readable.make_separator import make_separator
from mykit.kit.readable.time_quick import time_quick
from mykit.ghactions.eLog import eL
from mykit.kit.fileops.simple import list_dir
from mykit.kit.fileops.nice_io import NiceIO
from mykit.kit.readable.time_quick import time_quick

from TurboTest.core.chemicals import Container


class C:  # Constants

    T0 = time.time()
    CWD = os.getcwd()


class R:  # Runtime

    nPass = 0
    nFail = 0
    t_core = 0  # in seconds

    details = []


# def run_tester(module, function):
def run_tester(__TT_module, __TT_function):
    ## Docs: the "__TT_" prefix is used to make sure these function
    ##       args' variables will not conflict with the called function
    ##       `__TT_function` inside `locals()`.
    ## Note: the "__TT_" prefix is actually double checker, even though
    ##       `__TT_function` will never let in the functions that start
    ##       with an underscore (_), since functions that start with an
    ##       underscore are not considered as testers.

    # def wrap():
    #     print(f"locals before: {locals()}")
    #     exec(f'from {module} import {function}')
    #     print(f"locals after : {locals()}")
    # wrap()
    # vvvvvvvvvvvvvvvvvvv wrapping as shown above still allows access to `module` and `function` within the `locals()` scope

    # exec(f"{function}()")  # Testing purposes
    # print(f"nChem: {repr(Container.nChemical)}")
    # print(f"locals before: {locals()}")
    exec(f'from {__TT_module} import {__TT_function}')
    # print(f"locals after : {locals()}")
    exec(f"{__TT_function}()")
    # print(f"nChem: {repr(Container.nChemical)}")

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
                    # print(f'funcs={funcs}  at {repr(pth)}')

                    # print(f"DEBUG: pth: {pth}")
                    module_name_a = os.path.relpath(pth, C.CWD)
                    module_name_b = os.path.relpath(pth, C.CWD).split(os.sep)
                    module_name_c = '.'.join(os.path.relpath(pth, C.CWD).split(os.sep))
                    module_name = '.'.join(os.path.relpath(pth, C.CWD).split(os.sep))[:-3]
                    # print(f"DEBUG: module_name_a: {module_name_a}")
                    # print(f"DEBUG: module_name_b: {module_name_b}")
                    # print(f"DEBUG: module_name_c: {module_name_c}")
                    # print(f"DEBUG: module_name  : {module_name}")
                    
                    for ff in funcs:
                        tester_t0 = time.time()
                        run_tester(module_name, ff)
                        tester_t1 = time.time() - tester_t0
                        print(f'[{TimeFmt.hour()}]: PASS: {module_name[:-5]}: {ff.replace("_", " ")}  ({Container.nChemical}🧪|{time_quick(tester_t1)})')
                        Container.clear_chemical()

                    ## Make sure there is no duplication of tester names (each tester must have a unique name)
                    
                    ## change "cant" to "can't", "dont" -> "don't"

                    ## make sure tester should have at least 1 chemical

def run_tests(cwd):

    recur(cwd)


def run():

    ## Debugging purposes
    # eL.debug(os.listdir(C.CWD))
    print(f"DEBUG: C.CWD: {C.CWD}")
    print(f"DEBUG: os.listdir(C.CWD): {os.listdir(C.CWD)}")


    sys.path.append(C.CWD)


    SEP = make_separator('─', length_backup=110)

    ## Header
    print(f'TurboTest... at {repr(C.CWD)}  ({TimeFmt.full()})')
    print(SEP)

    run_tests(C.CWD)

    # body = 'okay123'
    # print(body)

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
