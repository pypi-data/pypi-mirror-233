# import traceback as tb
import types
from typing import Type, Optional, Any

from TurboTest.core.chemicals import Container
from TurboTest.core.error_tt import ErrorTT


class these_will_raise:
    """Guarantee the given exception will be raised"""

    def __init__(self, exception:Exception, /) -> None:
        """
        Guarantee the given `exception` will be raised

        ## Params
        - `exception`: the expected exception

        ## Demo
        >>> import TurboTest as tt
        >>> with tt.these_will_raise(ValueError) as its: raise ValueError('foo123')
        >>> print(its.exception_msg)  # foo123
        """
    
        ## Metadata
        Container.add_chemical()

        self.exception = exception

        ## Runtime
        self.exc_val = None  # exception value

    def __enter__(self):
        return self

    def __exit__(self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[types.TracebackType]
    ) -> Optional[bool]:
        
        ## No exceptions were raised
        if exc_type is None:

            raise ErrorTT(f"No exceptions were raised; expecting {self.exception.__name__}.")

        ## An exception occurred
        else:

            if exc_type is not self.exception:
                raise ErrorTT(f"Oops! Wrong exception. Expected {self.exception.__name__}, got {exc_type.__name__}.")

            self.exc_val = exc_value.args

            return True  # to suppress the exception within the context

    @property
    def exception_value(self) -> Any:  # created merely for readability
        """
        ## Demo
        >>> import TurboTest as tt
        >>> with tt.these_will_raise(AssertionError) as its: raise AssertionError('foo', 222)
        >>> print(its.exception_value)  # ('foo', 222)
        """
        return self.exc_val

    @property
    def exception_msg(self) -> str:  # created merely for readability
        """
        ## Demo
        >>> import TurboTest as tt
        >>> with tt.these_will_raise(ValueError) as its: raise ValueError('hi mom')
        >>> print(its.exception_msg)  # hi mom
        """
        return str(self.exc_val[0])

    @property
    def exit_code(self) -> int:  # created merely for readability
        """
        ## Demo
        >>> import sys
        >>> import TurboTest as tt
        >>> with tt.these_will_raise(SystemExit) as its: sys.exit(21)
        >>> print(its.exit_code)  # 21
        """
        return int(self.exc_val[0])
