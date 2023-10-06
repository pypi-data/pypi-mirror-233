

def runtime_guard(n_test, n_pass, n_fail, t_core, t_total):

    if (n_pass + n_fail) != n_test:
        raise AssertionError
