"""
Utility classes to use with pytest unit tests and mocked methods
"""
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..constants import DEFAULT_ENCODING

MOCK_ERROR_MESSAGE = 'Mocked exception was raised'


# pylint: disable=too-few-public-methods
class MockCalledMethod:
    """
    Class to mock a method or function and check it's call arguments

    Monkeypatch instance of this class to the place and store call variables
    """
    call_count: 0
    args: List
    kwargs: Dict[Any, Any]
    return_value: Optional[Any]

    def __init__(self, return_value: Optional[Any] = None) -> None:
        self.call_count = 0
        self.args = []
        self.kwargs = []
        self.return_value = return_value

    def __call__(self, *args: List[Any], **kwargs: List[Any]) -> Optional[Any]:
        """
        Increment call count, store method arguments and return stored value
        """
        self.call_count += 1
        self.args.append(args)
        self.kwargs.append(kwargs)
        return self.return_value


# pylint: disable=too-few-public-methods
class MockReturnTrue(MockCalledMethod):
    """
    Mock a method to always return True
    """
    def __init__(self) -> None:
        super().__init__(return_value=True)


# pylint: disable=too-few-public-methods
class MockReturnFalse(MockCalledMethod):
    """
    Mock a method to always return False
    """
    def __init__(self) -> None:
        super().__init__(return_value=False)


# pylint: disable=too-few-public-methods
class MockReturnEmptyList(MockCalledMethod):
    """
    Mock a method to always return None
    """
    def __init__(self) -> None:
        super().__init__(return_value=[])


class MockCheckOutput(MockCalledMethod):
    """
    Mock calling subprocess.check_output and returning data read from a file instead
    """
    path: str
    encoding: str

    def __init__(self, path: Union[str, Path], encoding: str = DEFAULT_ENCODING) -> None:
        super().__init__()
        self.path = path
        self.encoding = encoding

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> bytes:
        """
        Call mocked check_output, storing call argument and returning data from self.path file
        """
        super().__call__(*args, **kwargs)
        with open(self.path, encoding=self.encoding) as handle:
            return bytes(handle.read(), encoding=self.encoding)


class MockRun(MockCalledMethod):
    """
    Mock running a CLI command with return code, stdout and stderr
    """
    encoding: str
    stdout: Optional[bytes]
    stderr: Optional[bytes]
    returncode: Optional[int]

    def __init__(self,
                 encoding: str = DEFAULT_ENCODING,
                 stdout: Optional[bytes] = None,
                 stderr: Optional[bytes] = None,
                 returncode: Optional[int] = None) -> None:
        super().__init__(returncode)
        self.encoding = encoding
        self.stdout = stdout if stdout else ''
        self.stderr = stderr if stderr else ''
        if isinstance(self.stdout, str):
            self.stdout = bytes(self.stdout, encoding=encoding)
        if isinstance(self.stderr, str):
            self.stderr = bytes(self.stderr, encoding=encoding)
        self.returncode = returncode if isinstance(returncode, int) else 0

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        """
        Mock calling the run() method, returning 'self' as mostly compatible object
        """
        super().__call__(*args, **kwargs)
        return self


class MockRunCommandLineOutput(MockRun):
    """
    Mock calling sys_toolkit.subprocess.run_command_lineoutput and returning data
    read from a file instead
    """
    path: Union[str, Path]
    encoding: str = DEFAULT_ENCODING
    stdout: Optional[bytes]
    stderr: Optional[bytes]
    returncode: Optional[int] = None

    def __init__(self,
                 path: Union[str, Path] = None,
                 encoding: str = DEFAULT_ENCODING,
                 stdout: Optional[bytes] = None,
                 stderr: Optional[bytes] = None,
                 returncode: Optional[int] = None) -> None:
        super().__init__(encoding, stdout, stderr, returncode)
        self.path = path
        self.encoding = encoding
        self.stdout = stdout if stdout else []
        self.stderr = stderr if stderr else ''

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Tuple[bytes, bytes]:
        """
        Call mocked check_output, storing call argument and returning data from self.path file
        """
        super().__call__(*args, **kwargs)
        if self.path is not None:
            with open(self.path, encoding=self.encoding) as handle:
                return handle.read().splitlines(), self.stderr
        return self.stdout, self.stderr


# pylint: disable=too-few-public-methods
class MockException(MockCalledMethod):
    """
    Mock raising specified exception when method is called. Stores call arguments just like
    MockCalledMethod before raising the exception

    Custom arguments to the raised exception can be passed with *args and **kwargs. If no
    arguments are passed exception and default_message is True, exception is raised with
    string MOCK_ERROR_MESSAGE, otherwise it's raised with on arguments
    """
    exception: Exception
    default_message: bool
    exception_kwargs: Dict[Any, Any]

    def __init__(self,
                 exception: Exception = Exception,
                 default_message: bool = True,
                 **exception_kwargs: Dict[Any, Any]) -> None:
        super().__init__()
        self.exception = exception
        self.default_message = default_message
        self.exception_kwargs = exception_kwargs if exception_kwargs else {}

    def __call__(self, *args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        """
        Store call arguments and raise specified exception with specified arguments
        or mocked message if nothing was specified
        """
        super().__call__(*args, **kwargs)
        if self.exception_kwargs:
            raise self.exception(**self.exception_kwargs)
        if self.default_message:
            raise self.exception(MOCK_ERROR_MESSAGE)
        raise self.exception
