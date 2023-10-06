from mykit.kit.color import Hex, Colored
from mykit.kit.time import TimeFmt


def print_footer(n_test, n_pass, n_fail, t_core_formatted, t_total_formatted):

    ## No issues
    if n_fail == 0:
        footer = (
            f'Done @ {TimeFmt.hour()}, 🎉All {Colored(n_test, Hex.EMERALD)} '
             'test functions executed successfully in '
            f'[core/total: {t_core_formatted}/{t_total_formatted}] 🔥🔥'
        )

    ## Some issues detected
    else:
        footer = (
            f'Done @ {TimeFmt.hour()}, {n_test} test functions '
            f'[pass/fail: {Colored(n_pass, Hex.EMERALD)}/{Colored(n_fail, Hex.SCARLET)}] '
             'executed in '
            f'[core/total: {t_core_formatted}/{t_total_formatted}] 🔥🔥'
        )

    print(footer)
