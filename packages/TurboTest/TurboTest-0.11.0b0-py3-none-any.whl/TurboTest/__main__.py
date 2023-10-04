try:
    from TurboTest.runner import run
except ImportError:  # local dev
    import sys, os
    sys.path.append(os.path.dirname(__file__))
    from runner import run
if __name__=='__main__':run()
