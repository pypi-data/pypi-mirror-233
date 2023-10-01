"""A tool to automatically format Python docstrings."""
import os
import sys

from celestine import load
from celestine.typed import (
    MT,
    N,
    S,
)

from . import Abstract


class Package(Abstract):
    """"""

    def main(self, package: MT, path: S) -> N:
        """
        This package is troublesome.

        It can't find the pyproject file unless run from root directory.
        Exclude argument simply does not work.
        Manually feeding it files works.
        """

        location = os.getcwd()
        os.chdir(sys.path[0])

        files = load.many.python(path, [], ["unicode"])

        file = map(str, files)
        argv = [*file]
        package.run_docstring_formatter(argv)

        os.chdir(location)
