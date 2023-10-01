# pygamecfg (c) by chacha
#
# pygamecfg  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

import unittest
from os import chdir
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from src import pygamecfg
from src.pygamecfg.__main__ import fct_main


testdir_path = Path(__file__).parent.resolve()


class Testtest_gen(unittest.TestCase):
    def setUp(self) -> None:
        chdir(testdir_path.parent.resolve())

    def test_version(self):
        self.assertNotEqual(pygamecfg.__version__, "?.?.?")

    def test_normal_help(self):
        with self.assertRaises(SystemExit) as cm:
            fct_main(["-h"])

    def test_defect_nogame(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            with self.assertRaises(SystemExit) as cm:
                fct_main(["GetOption", "test"])
            self.assertIn("pygamecfg: error: the following arguments are required: -g/--game", capted_stderr.getvalue())
            self.assertIn("", capted_stdout.getvalue())
