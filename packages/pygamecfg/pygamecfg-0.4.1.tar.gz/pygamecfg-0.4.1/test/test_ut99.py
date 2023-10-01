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

testdir_path = Path(__file__).parent.resolve()


class Testtest_ut99(unittest.TestCase):
    def setUp(self) -> None:
        chdir(testdir_path.parent.resolve())
        self.CleanTmp()
        shutil.copytree(testdir_path / "data", testdir_path / "tmp")
        print("======================")

    def CleanTmp(self):
        # remove any file in tmp dir, except .keep
        if path.exists(testdir_path / "tmp"):
            shutil.rmtree(testdir_path / "tmp")

    def test_normal_ServerPackages(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "ServerPackages"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual(
                "['SoldierSkins', 'CommandoSkins', 'FCommandoSkins', 'SGirlSkins', 'BossSkins', 'Botpack']\n", capted_stdout.getvalue()
            )
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_ServerActors(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "ServerActors"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual(
                "['IpDrv.UdpBeacon', 'IpServer.UdpServerQuery', 'IpServer.UdpServerUplink MasterServerAddress=unreal.epicgames.com MasterServerPort=27900', 'IpServer.UdpServerUplink MasterServerAddress=master0.gamespy.com MasterServerPort=27900', 'IpServer.UdpServerUplink MasterServerAddress=master.mplayer.com MasterServerPort=27900', 'UWeb.WebServer']\n",
                capted_stdout.getvalue(),
            )
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_Port(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "Port"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("7777\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_Map(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "Map"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("Index.unr\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_GameType(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "GameType"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("Botpack.DeathMatchPlus\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_HostName(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "HostName"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("Test Server Name FULL\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MOTD(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MOTD"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestMOTDLine1\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MOTD2(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MOTD2"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestMOTDLine2\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MOTD3(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MOTD3"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestMOTDLine3\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MOTD4(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MOTD4"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestMOTDLine4\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_AdminEmail(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "AdminEmail"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestAdminName@test.com\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_AdminName(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "AdminName"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestAdminName\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_HTTPDownloadServer(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "HTTPDownloadServer"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("http://uz.ut-files.com/\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MaxClientRate(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MaxClientRate"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("20000\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_NetServerMaxTickRate(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "NetServerMaxTickRate"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("20\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_LanServerMaxTickRate(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "LanServerMaxTickRate"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("35\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_AdminPassword(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "AdminPassword"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestAdminPwd\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_GamePassword(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "GamePassword"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("TestPwd\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MaxPlayers(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MaxPlayers"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("4\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MaxSpectators(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MaxSpectators"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("1\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_AS_TimeLimit(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "AS_TimeLimit"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("123\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DOM_TimeLimit(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DOM_TimeLimit"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("423\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_CTF_TimeLimit(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "CTF_TimeLimit"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("223\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DM_TimeLimit(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DM_TimeLimit"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("323\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_GoalTeamScore(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "GoalTeamScore"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("30\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MaxTeamSize(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MaxTeamSize"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("4\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DM_FragLimit(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DM_FragLimit"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("321\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_ServerLogName(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "ServerLogName"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("server.log\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_WebServer(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "WebServer"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("9999\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_TournamentMode(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "TournamentMode"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("False\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_InitialBots(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "InitialBots"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("7\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_MinPlayers(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "MinPlayers"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("11\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_AS_UseTranslocator(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "AS_UseTranslocator"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("True\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_CTF_UseTranslocator(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "CTF_UseTranslocator"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("True\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DM_UseTranslocator(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DM_UseTranslocator"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("False\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DOM_UseTranslocator(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DOM_UseTranslocator"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("True\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_CTF_ForceRespawn(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "CTF_ForceRespawn"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("False\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DM_ForceRespawn(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DM_ForceRespawn"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("True\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_DOM_ForceRespawn(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "DOM_ForceRespawn"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("False\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_AS_ForceRespawn(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "GetOption", "AS_ForceRespawn"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("True\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())

    def test_normal_customcfgfile_HostName(self):
        with redirect_stdout(StringIO()) as capted_stdout, redirect_stderr(StringIO()) as capted_stderr:
            fct_main(["-g", "ut99", "-b", "test/tmp/UT99", "-c", "System/UT99.ini", "GetOption", "HostName"])
            # /!\ add '\n' at the end of the string cause Python terminal newline is always this, regardless Windows / Linux os.linesep
            self.assertEqual("Alt Serv Name FULL\n", capted_stdout.getvalue())
            self.assertEqual("", capted_stderr.getvalue())
