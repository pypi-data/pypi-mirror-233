# pygamecfg (c) by chacha
#
# pygamecfg  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

import unittest
from os import path, chdir
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import shutil

from src import pygamecfg
from src.pygamecfg.__main__ import fct_main
from src.pygamecfg.game_cod4 import COD4KeyNotFoundError

testdir_path = Path(__file__).parent.resolve()


class Testtest_cod4(unittest.TestCase):
    def setUp(self) -> None:
        chdir(testdir_path.parent.resolve())
        self.CleanTmp()
        shutil.copytree(testdir_path / "data", testdir_path / "tmp")
        print("======================")

    def CleanTmp(self):
        # remove any file in tmp dir, except .keep
        if path.exists(testdir_path / "tmp"):
            shutil.rmtree(testdir_path / "tmp")

    def test_normal_READ_sv_maxclients(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "maxclients"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("11\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_READ_sv_mapRotation(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "mapRotation"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual(
                "gametype dm map mp_backlot gametype dm map mp_bloc gametype dm map mp_bog gametype dm map mp_cargoship gametype dm map mp_citystreets gametype dm map mp_convoy gametype dm map mp_countdown gametype dm map mp_crash gametype dm map mp_crossfire gametype dm map mp_farm gametype dm map mp_overgrown gametype dm map mp_pipeline gametype dm map mp_shipment gametype dm map mp_showdown gametype dm map mp_strike gametype dm map mp_vacant\n",
                capted_stdout.getvalue(),
            )
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_WRITE_sv_maxclients(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "SetOption", "maxclients", "17"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("setting option <maxclients>  to:  17\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "maxclients"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("17\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())
        # check if *other* key still there / untouched
        self.test_normal_READ_sv_mapRotation()

    def test_defect_READ_net_port_NONEXISTS(self):
        with self.assertRaises(COD4KeyNotFoundError):
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "net_port"])

    def test_normal_WRITE_net_port_NONEXISTS(self):
        fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "SetOption", "net_port", "132"])
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "net_port"])
            self.assertEqual("132\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_WRITE_oldschool(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "SetOption", "oldschool", "1"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("setting option <oldschool>  to:  1\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "oldschool"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("1\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "SetOption", "oldschool", "0"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("setting option <oldschool>  to:  0\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "oldschool"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("0\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "SetOption", "oldschool", "1"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("setting option <oldschool>  to:  1\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "cod4", "-b", "test/tmp/COD4", "GetOption", "oldschool"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("1\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())
