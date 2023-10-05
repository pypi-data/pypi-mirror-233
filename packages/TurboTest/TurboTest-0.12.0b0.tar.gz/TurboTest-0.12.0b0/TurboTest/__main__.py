## <for local dev>
try:
    from .runner import run
except ImportError:  # occur during local dev
    import sys, os
    sys.path.append(os.path.dirname(__file__))
    from runner import run
## </for local dev>

# from .runner import run
if __name__=='__main__':run()