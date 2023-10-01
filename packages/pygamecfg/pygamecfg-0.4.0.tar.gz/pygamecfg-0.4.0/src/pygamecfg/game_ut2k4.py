#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

# pylint: disable=missing-class-docstring,missing-function-docstring,duplicate-code,line-too-long
"""UT2k4 command set"""
from __future__ import annotations
from typing import Union

from pysimpleini import KeyNotFoundError

from .core_gamecfg import GameOptions_Factory_Register, OptionType
from .tool_ini import PySimpleINI_GroupKeysInSection
from .common_ut import GameOption_UT


class PySimpleINI_UT2k4(PySimpleINI_GroupKeysInSection):
    GroupRules = [
        ("Engine.GameEngine", "ServerPackages"),
        ("Engine.GameEngine", "ServerActors"),
        ("Core.System", "Suppress"),
        ("Core.System", "Paths"),
        ("Core.System", "Paths"),
        ("Editor.EditorEngine", "EditPackages"),
        ("Editor.EditorEngine", "CutdownPackages"),
    ]


class GameOption_UT2k4(GameOption_UT):
    szGameType = "ut2k4"
    Cls_PySimpleINI = PySimpleINI_UT2k4


class GameOption_UT2k4_GenAdd(GameOption_UT2k4):
    bForceAdd = True

    def rem(self, value: Union[None, str]) -> None:
        try:
            super().rem(value)
        except KeyNotFoundError:
            pass

    def set(self, value: str) -> None:
        # force to call the rem method of THIS level
        GameOption_UT2k4_GenAdd.rem(self, value)
        super().set(value)


class GameOption_UT2k4_GenAdd__Engine(GameOption_UT2k4_GenAdd):
    szSectionName = "Engine.GameEngine"
    TValueType = OptionType.OT_STRING
    bRemovable = True


@GameOptions_Factory_Register
class GameOption_UT2k4_ServerPackages(GameOption_UT2k4_GenAdd__Engine):
    szOptionName = "ServerPackages"
    szKeyName = "ServerPackages"
    szHelp = "Add a ServerPackages record"


@GameOptions_Factory_Register
class GameOption_UT2k4_ServerActors(GameOption_UT2k4_GenAdd__Engine):
    szOptionName = "ServerActors"
    szKeyName = "ServerActors"
    szHelp = "Add a ServerActors record"


@GameOptions_Factory_Register
class GameOption_UT2k4_MasterServerList(GameOption_UT2k4_GenAdd):
    szSectionName = "IpDrv.MasterServerLink"
    TValueType = OptionType.OT_STRING
    bRemovable = True
    szOptionName = "MasterServerList"
    szKeyName = "MasterServerList"
    szHelp = "Add a MasterServerList record"


@GameOptions_Factory_Register
class GameOption_UT2k4_Port(GameOption_UT2k4):
    szOptionName = "Port"
    szSectionName = "URL"
    szKeyName = "Port"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "7777"
    szHelp = "Server Listening port"


@GameOptions_Factory_Register
class GameOption_UT2k4_Map(GameOption_UT2k4):
    szOptionName = "Map"
    szSectionName = "URL"
    szKeyName = "Map"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "dm-deck16]["
    szHelp = "Server Map"


@GameOptions_Factory_Register
class GameOption_UT2k4_GameType(GameOption_UT2k4):
    szOptionName = "GameType"
    szSectionName = "Engine.Engine"
    szKeyName = "DefaultServerGame"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "XGame.XDeathmatch"
    szHelp = "Server Gametype"


@GameOptions_Factory_Register
class GameOption_UT2k4_HostName(GameOption_UT2k4):
    szOptionName = "HostName"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "ServerName"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "ChaCha Test Server"
    szHelp = "Server's HostName"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("Engine.GameReplicationInfo", "ShortName", value)
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT2k4_MOTD(GameOption_UT2k4):
    szOptionName = "MOTD"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "MessageOfTheDay"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "Welcome to ChaCha's server"
    szHelp = "Message of the day"


@GameOptions_Factory_Register
class GameOption_UT2k4_AdminEmail(GameOption_UT2k4):
    szOptionName = "AdminEmail"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "AdminEmail"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "chachacorp@protonmail.com"
    szHelp = "Admin mail"


@GameOptions_Factory_Register
class GameOption_UT2k4_AdminName(GameOption_UT2k4):
    szOptionName = "AdminName"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "AdminName"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "chacha"
    szHelp = "Admin name"


@GameOptions_Factory_Register
class GameOption_UT2k4_HTTPDownloadServer(GameOption_UT2k4):
    szOptionName = "HTTPDownloadServer"
    szSectionName = "IpDrv.HTTPDownload"
    szKeyName = "RedirectToURL"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "http://chacha.ddns.net/games/ut2k4"
    szHelp = "FastDL url"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("IpDrv.HTTPDownload", "UseCompression", "True")
        self.inifile.delkey("IpDrv.HTTPDownload", "ProxyServerHost")
        self.inifile.delkey("IpDrv.HTTPDownload", "ProxyServerPort")
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT2k4_MaxClientRate(GameOption_UT2k4):
    szOptionName = "MaxClientRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "MaxClientRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "25000"
    szHelp = "Max Client Rate"


@GameOptions_Factory_Register
class GameOption_UT2k4_MaxInternetClientRate(GameOption_UT2k4):
    szOptionName = "MaxInternetClientRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "MaxClientRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "25000"
    szHelp = "Max Client Rate"


@GameOptions_Factory_Register
class GameOption_UT2k4_NetServerMaxTickRate(GameOption_UT2k4):
    szOptionName = "NetServerMaxTickRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "NetServerMaxTickRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "60"
    szHelp = "Server Max TickRate"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("Engine.DemoRecDrive", "NetServerMaxTickRate", value)
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT2k4_LanServerMaxTickRate(GameOption_UT2k4):
    szOptionName = "LanServerMaxTickRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "LanServerMaxTickRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "60"
    szHelp = "Lan Server Max TickRate"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("Engine.DemoRecDrive", "LanServerMaxTickRate", value)
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT2k4_AdminPassword(GameOption_UT2k4):
    szOptionName = "AdminPassword"
    szSectionName = "Engine.AccessControl"
    szKeyName = "AdminPassword"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "cfographut"
    szHelp = "Admin password"


@GameOptions_Factory_Register
class GameOption_UT2k4_GamePassword(GameOption_UT2k4):
    szOptionName = "GamePassword"
    szSectionName = "Engine.AccessControl"
    szKeyName = "GamePassword"
    TValueType = OptionType.OT_STRING
    szDefaultValue = ""
    szHelp = "Game password"


@GameOptions_Factory_Register
class GameOption_UT2k4_MaxPlayers(GameOption_UT2k4):
    szOptionName = "MaxPlayers"
    szSectionName = "Engine.GameInfo"
    szKeyName = "MaxPlayers"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Max Players"


@GameOptions_Factory_Register
class GameOption_UT2k4_MaxSpectators(GameOption_UT2k4):
    szOptionName = "MaxSpectators"
    szSectionName = "Engine.GameInfo"
    szKeyName = "MaxSpectators"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Max Spectators"


##############
## TimeLimit
#############
class GameOption_UT2k4_TimeLimit(GameOption_UT2k4):
    szOptionName = "TimeLimit"
    szKeyName = "TimeLimit"
    TValueType = OptionType.OT_INTEGER
    szHelp = "Game Time Limit"


@GameOptions_Factory_Register
class GameOption_UT2k4_CTF_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "CTF_TimeLimit"
    szSectionName = "xGame.xCTFGame"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_DM_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "DM_TimeLimit"
    szSectionName = "XGame.xDeathMatch"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_TDM_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "TDM_TimeLimit"
    szSectionName = "XGame.xTeamGame"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_ONS_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "ONS_TimeLimit"
    szSectionName = "Onslaught.ONSOnslaughtGame"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_DOM_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "DOM_TimeLimit"
    szSectionName = "XGame.xDoubleDom"
    szDefaultValue = "3"


@GameOptions_Factory_Register
class GameOption_UT2k4_BR_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "BR_TimeLimit"
    szSectionName = "XGame.xBombingRun"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_AS_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "AS_TimeLimit"
    szSectionName = "UT2k4Assault.ASGameInfo"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_LMS_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "LMS_TimeLimit"
    szSectionName = "BonusPack.xLastManStandingGame"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_INV_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "INV_TimeLimit"
    szSectionName = "SkaarjPack.Invasion"
    szDefaultValue = "20"


@GameOptions_Factory_Register
class GameOption_UT2k4_MUT_TimeLimit(GameOption_UT2k4_TimeLimit):
    szOptionName = "MUT_TimeLimit"
    szSectionName = "BonusPack.xMutantGame"
    szDefaultValue = "20"


##############
## GoalScore
#############
class GameOption_UT2k4_GoalScore(GameOption_UT2k4):
    szOptionName = "GoalScore"
    szKeyName = "GoalScore"
    TValueType = OptionType.OT_INTEGER
    szHelp = "Game Score Goal"


@GameOptions_Factory_Register
class GameOption_UT2k4_CTF_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "CTF_GoalScore"
    szSectionName = "xGame.xCTFGame"
    szDefaultValue = "5"


@GameOptions_Factory_Register
class GameOption_UT2k4_DM_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "DM_GoalScore"
    szSectionName = "XGame.xDeathMatch"
    szDefaultValue = "25"


@GameOptions_Factory_Register
class GameOption_UT2k4_TDM_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "TDM_GoalScore"
    szSectionName = "XGame.xTeamGame"
    szDefaultValue = "60"


@GameOptions_Factory_Register
class GameOption_UT2k4_ONS_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "ONS_GoalScore"
    szSectionName = "Onslaught.ONSOnslaughtGame"
    szDefaultValue = "3"


@GameOptions_Factory_Register
class GameOption_UT2k4_DOM_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "DOM_GoalScore"
    szSectionName = "XGame.xDoubleDom"
    szDefaultValue = "3"


@GameOptions_Factory_Register
class GameOption_UT2k4_BR_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "BR_GoalScore"
    szSectionName = "XGame.xBombingRun"
    szDefaultValue = "15"


@GameOptions_Factory_Register
class GameOption_UT2k4_AS_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "AS_GoalScore"
    szSectionName = "UT2k4Assault.ASGameInfo"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_LMS_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "LMS_GoalScore"
    szSectionName = "BonusPack.xLastManStandingGame"
    szDefaultValue = "25"


@GameOptions_Factory_Register
class GameOption_UT2k4_INV_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "INV_GoalScore"
    szSectionName = "SkaarjPack.Invasion"
    szDefaultValue = "60"


@GameOptions_Factory_Register
class GameOption_UT2k4_MUT_GoalScore(GameOption_UT2k4_GoalScore):
    szOptionName = "MUT_GoalScore"
    szSectionName = "BonusPack.xMutantGame"
    szDefaultValue = "20"


##############
## ForceRespawn
#############
class GameOption_UT2k4_ForceRespawn(GameOption_UT2k4):
    szOptionName = "ForceRespawn"
    szKeyName = "bForceRespawn"
    TValueType = OptionType.OT_BOOLEAN
    szHelp = "Force player to Respawn"


@GameOptions_Factory_Register
class GameOption_UT2k4_CTF_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "CTF_ForceRespawn"
    szSectionName = "xGame.xCTFGame"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_DM_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "DM_ForceRespawn"
    szSectionName = "XGame.xDeathMatch"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_TDM_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "TDM_ForceRespawn"
    szSectionName = "XGame.xTeamGame"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_ONS_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "ONS_ForceRespawn"
    szSectionName = "Onslaught.ONSOnslaughtGame"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_DOM_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "DOM_ForceRespawn"
    szSectionName = "XGame.xDoubleDom"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_BR_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "BR_ForceRespawn"
    szSectionName = "XGame.xBombingRun"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_AS_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "AS_ForceRespawn"
    szSectionName = "UT2k4Assault.ASGameInfo"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_LMS_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "LMS_ForceRespawn"
    szSectionName = "BonusPack.xLastManStandingGame"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_INV_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "INV_ForceRespawn"
    szSectionName = "SkaarjPack.Invasion"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_MUT_ForceRespawn(GameOption_UT2k4_ForceRespawn):
    szOptionName = "MUT_ForceRespawn"
    szSectionName = "BonusPack.xMutantGame"
    szDefaultValue = "True"


##############
## MaxLives
#############
class GameOption_UT2k4_MaxLives(GameOption_UT2k4):
    szOptionName = "MaxLives"
    szKeyName = "MaxLives"
    TValueType = OptionType.OT_INTEGER
    szHelp = "Maximum player lives"


@GameOptions_Factory_Register
class GameOption_UT2k4_CTF_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "CTF_MaxLives"
    szSectionName = "xGame.xCTFGame"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_DM_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "DM_MaxLives"
    szSectionName = "XGame.xDeathMatch"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_TDM_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "TDM_MaxLives"
    szSectionName = "XGame.xTeamGame"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_ONS_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "ONS_MaxLives"
    szSectionName = "Onslaught.ONSOnslaughtGame"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_DOM_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "DOM_MaxLives"
    szSectionName = "XGame.xDoubleDom"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_BR_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "BR_MaxLives"
    szSectionName = "XGame.xBombingRun"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_AS_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "AS_MaxLives"
    szSectionName = "UT2k4Assault.ASGameInfo"
    szDefaultValue = "0"


@GameOptions_Factory_Register
class GameOption_UT2k4_LMS_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "LMS_MaxLives"
    szSectionName = "BonusPack.xLastManStandingGame"
    szDefaultValue = "4"


@GameOptions_Factory_Register
class GameOption_UT2k4_INV_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "INV_MaxLives"
    szSectionName = "SkaarjPack.Invasion"
    szDefaultValue = "4"


@GameOptions_Factory_Register
class GameOption_UT2k4_MUT_MaxLives(GameOption_UT2k4_MaxLives):
    szOptionName = "MUT_MaxLives"
    szSectionName = "BonusPack.xMutantGame"
    szDefaultValue = "0"


##############
## AllowTrans
#############
class GameOption_UT2k4_AllowTrans(GameOption_UT2k4):
    szOptionName = "AllowTrans"
    szKeyName = "bAllowTrans"
    TValueType = OptionType.OT_BOOLEAN
    szHelp = "Maximum player lives"


@GameOptions_Factory_Register
class GameOption_UT2k4_CTF_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "CTF_AllowTrans"
    szSectionName = "xGame.xCTFGame"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_DM_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "DM_AllowTrans"
    szSectionName = "XGame.xDeathMatch"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_TDM_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "TDM_AllowTrans"
    szSectionName = "XGame.xTeamGame"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_ONS_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "ONS_AllowTrans"
    szSectionName = "Onslaught.ONSOnslaughtGame"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_DOM_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "DOM_AllowTrans"
    szSectionName = "XGame.xDoubleDom"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_BR_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "BR_AllowTrans"
    szSectionName = "XGame.xBombingRun"
    szDefaultValue = "True"


@GameOptions_Factory_Register
class GameOption_UT2k4_AS_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "AS_AllowTrans"
    szSectionName = "UT2k4Assault.ASGameInfo"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_LMS_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "LMS_AllowTrans"
    szSectionName = "BonusPack.xLastManStandingGame"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_INV_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "INV_AllowTrans"
    szSectionName = "SkaarjPack.Invasion"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_MUT_AllowTrans(GameOption_UT2k4_AllowTrans):
    szOptionName = "MUT_AllowTrans"
    szSectionName = "BonusPack.xMutantGame"
    szDefaultValue = "False"


@GameOptions_Factory_Register
class GameOption_UT2k4_WebServer_ServerName(GameOption_UT2k4):
    szOptionName = "WebServer_ServerName"
    szSectionName = "UWeb.WebServer"
    szKeyName = "ServerName"
    TValueType = OptionType.OT_STRING
    szDefaultValue = ""
    szHelp = "Server external IP or Name"


@GameOptions_Factory_Register
class GameOption_UT2k4_ServerBehindNAT(GameOption_UT2k4):
    szOptionName = "ServerBehindNAT"
    szSectionName = "IpDrv.MasterServerUplink"
    szKeyName = "ServerBehindNAT"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "False"
    szHelp = "Is server behind a NAS ?"


@GameOptions_Factory_Register
class GameOption_UT2k4_WebServer(GameOption_UT2k4):
    szOptionName = "WebServer"
    szSectionName = "UWeb.WebServer"
    szKeyName = "ListenPort"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "8080"
    szHelp = "enable Web Server"

    def set(self, value: str) -> None:
        super().set(value)
        if int(value) > 0:
            self.inifile.setaddkeyvalue("UWeb.WebServer", "bEnabled", "True")
        else:
            self.inifile.setaddkeyvalue("UWeb.WebServer", "bEnabled", "False")
        self.inifile.writefile()
