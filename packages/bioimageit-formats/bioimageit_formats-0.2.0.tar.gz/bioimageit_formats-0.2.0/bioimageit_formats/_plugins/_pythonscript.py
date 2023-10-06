import sys
from .._reader import FormatReader


class PythonScriptServiceBuilder:
    """Service builder for the python script reader"""

    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = PythonScriptReaderService()
        return self._instance


class PythonScriptReaderService(FormatReader):
    """Reader for python script

    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def read(filename):
        with open(filename, "r") as f:
            s = f.read()
            print(s)
        return imread(s)
