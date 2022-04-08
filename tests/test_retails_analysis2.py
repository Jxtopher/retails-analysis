from retails_analysis import __version__
from unittest import TestCase


class ManageParallelRunTest(TestCase):

    def test_run_parallel(self) -> None:
        assert __version__ == '0.1.0'