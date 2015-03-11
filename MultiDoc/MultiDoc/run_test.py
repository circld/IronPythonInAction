"""
If using relative imports (ie, from ..App.opencommands import OpenCommand)
then must run script from ... directory:

>>> ipy64.exe -m MultiDoc.Test.unit_tests

Otherwise, and probably more simply, include a script at the parent
directory level and use the more straightforward App.opencommands
form for importing (see Test.unit_tests.py).

Takeaway: where you run the test script from matters, so take the
guesswork out by 'hardcoding' it in a script.
"""

from Test.unit_tests import ut, test_OpenFileDialog


if __name__ == '__main__':
    ut.main()
