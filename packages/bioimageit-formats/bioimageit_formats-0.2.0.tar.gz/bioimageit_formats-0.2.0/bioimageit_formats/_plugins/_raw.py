from skimage.io import imread
from .._reader import FormatReader


class RawServiceBuilder:
    """Service builder for the raw reader"""

    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = RawReaderService()
        return self._instance


class RawReaderService(FormatReader):
    """Reader for Raw images

    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def read(filename):
        return filename
