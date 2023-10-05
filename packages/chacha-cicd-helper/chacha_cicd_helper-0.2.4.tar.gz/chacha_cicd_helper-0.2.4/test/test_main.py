# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

import unittest
from os import chdir
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

print(__name__)
print(__package__)

from src import chacha_cicd_helper
from src.chacha_cicd_helper.__main__ import fct_main

testdir_path = Path(__file__).parent.resolve()


class Test_main(unittest.TestCase):
    def setUp(self) -> None:
        chdir(testdir_path.parent.resolve())
        print("======================")

    def test_version(self):
        self.assertNotEqual(chacha_cicd_helper.__version__, "?.?.?")

    def test_help(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            with self.assertRaises(SystemExit):
                fct_main(["-h", "-pp", str(testdir_path.parent.resolve())])
        self.assertIn(f"usage: {chacha_cicd_helper.__Name__}", capted_stdout.getvalue())
        self.assertEqual(capted_stderr.getvalue(), "")

    @unittest.skip
    def test_help_print(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["--typecheck"])
            # fct_main(["-h", "-pp", str(testdir_path.parent.resolve())])
        print(capted_stdout.getvalue())
        print(capted_stderr.getvalue())
