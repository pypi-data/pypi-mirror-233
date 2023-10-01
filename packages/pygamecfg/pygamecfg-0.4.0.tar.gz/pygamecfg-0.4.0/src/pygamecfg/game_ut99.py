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
"""UT99 command set"""
from __future__ import annotations
from typing import Union

from pysimpleini import KeyNotFoundError, SectionNotFoundError

from .core_gamecfg import GameOptions_Factory_Register, OptionType
from .tool_ini import PySimpleINI_GroupKeysInSection
from .common_ut import GameOption_UT


class PySimpleINI_UT99(PySimpleINI_GroupKeysInSection):
    GroupRules = [
        ("XC_Engine.XC_GameEngine", "ServerPackages"),
        ("XC_Engine.XC_GameEngine", "ServerActors"),
        ("Engine.GameEngine", "ServerPackages"),
        ("Engine.GameEngine", "ServerActors"),
        ("Core.System", "Suppress"),
        ("Editor.EditorEngine", "EditPackages"),
    ]


class GameOption_UT99(GameOption_UT):
    szGameType = "ut99"
    Cls_PySimpleINI = PySimpleINI_UT99


class GameOption_UT99_GenAdd(GameOption_UT99):
    bForceAdd = True

    def rem(self, value: Union[None, str]) -> None:
        try:
            super().rem(value)
        except KeyNotFoundError:
            pass

    def set(self, value: str) -> None:
        # force to call the rem method of THIS level
        GameOption_UT99_GenAdd.rem(self, value)
        super().set(value)


class GameOption_UT99_GenAdd__Engine(GameOption_UT99_GenAdd):
    szSectionName = "Engine.GameEngine"
    TValueType = OptionType.OT_STRING
    bRemovable = True

    def set(self, value: str) -> None:
        prev = self.szSectionName

        try:
            self.inifile.getsection("XC_Engine.XC_GameEngine")
            self.szSectionName = "XC_Engine.XC_GameEngine"
            super().set(value)
        except SectionNotFoundError:
            pass

        self.szSectionName = "Engine.GameEngine"
        super().set(value)
        self.szSectionName = prev

    def rem(self, value: Union[None, str]) -> None:
        prev = self.szSectionName

        try:
            self.inifile.getsection("XC_Engine.XC_GameEngine")
            self.szSectionName = "XC_Engine.XC_GameEngine"
            super().rem(value)
        except SectionNotFoundError:
            pass
        self.szSectionName = "Engine.GameEngine"
        super().rem(value)
        self.szSectionName = prev


@GameOptions_Factory_Register
class GameOption_UT99_ServerPackages(GameOption_UT99_GenAdd__Engine):
    szOptionName = "ServerPackages"
    szKeyName = "ServerPackages"
    szHelp = "Add a ServerPackages record"


@GameOptions_Factory_Register
class GameOption_UT99_ServerActors(GameOption_UT99_GenAdd__Engine):
    szOptionName = "ServerActors"
    szKeyName = "ServerActors"
    szHelp = "Add a ServerActors record"


@GameOptions_Factory_Register
class GameOption_UT99_Port(GameOption_UT99):
    szOptionName = "Port"
    szSectionName = "URL"
    szKeyName = "Port"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "7777"
    szHelp = "Server Listening port"


@GameOptions_Factory_Register
class GameOption_UT99_Map(GameOption_UT99):
    szOptionName = "Map"
    szSectionName = "URL"
    szKeyName = "Map"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "dm-deck16]["
    szHelp = "Server Map"


@GameOptions_Factory_Register
class GameOption_UT99_GameType(GameOption_UT99):
    szOptionName = "GameType"
    szSectionName = "Engine.Engine"
    szKeyName = "DefaultServerGame"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "Botpack.DeathMatchPlus"
    szHelp = "Server Gametype"


@GameOptions_Factory_Register
class GameOption_UT99_HostName(GameOption_UT99):
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
class GameOption_UT99_MOTD(GameOption_UT99):
    szOptionName = "MOTD"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "MOTDLine1"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "Welcome to ChaCha's server"
    szHelp = "Message of the day"


@GameOptions_Factory_Register
class GameOption_UT99_MOTD2(GameOption_UT99):
    szOptionName = "MOTD2"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "MOTDLine2"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "Enjoy your stay and have fun"
    szHelp = "Message of the day (2)"


@GameOptions_Factory_Register
class GameOption_UT99_MOTD3(GameOption_UT99):
    szOptionName = "MOTD3"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "MOTDLine3"
    TValueType = OptionType.OT_STRING
    szDefaultValue = ""
    szHelp = "Message of the day (3)"


@GameOptions_Factory_Register
class GameOption_UT99_MOTD4(GameOption_UT99):
    szOptionName = "MOTD4"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "MOTDLine4"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "Game Server by ChaCha"
    szHelp = "Message of the day (4)"


@GameOptions_Factory_Register
class GameOption_UT99_AdminEmail(GameOption_UT99):
    szOptionName = "AdminEmail"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "AdminEmail"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "chachacorp@protonmail.com"
    szHelp = "Admin mail"


@GameOptions_Factory_Register
class GameOption_UT99_AdminName(GameOption_UT99):
    szOptionName = "AdminName"
    szSectionName = "Engine.GameReplicationInfo"
    szKeyName = "AdminName"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "chacha"
    szHelp = "Admin name"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("UTServerAdmin.UTServerAdmin", "AdminUsername", value)
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT99_HTTPDownloadServer(GameOption_UT99):
    szOptionName = "HTTPDownloadServer"
    szSectionName = "IpDrv.HTTPDownload"
    szKeyName = "RedirectToURL"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "http://chacha.ddns.net/games/ut99"
    szHelp = "FastDL url"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("IpDrv.HTTPDownload", "UseCompression", "True")
        self.inifile.delkey("IpDrv.HTTPDownload", "ProxyServerHost")
        self.inifile.delkey("IpDrv.HTTPDownload", "ProxyServerPort")
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT99_MaxClientRate(GameOption_UT99):
    szOptionName = "MaxClientRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "MaxClientRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "25000"
    szHelp = "Max Client Rate"


@GameOptions_Factory_Register
class GameOption_UT99_MinClientRate(GameOption_UT99):
    szOptionName = "MinClientRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "MinClientRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "12000"
    szHelp = "Max Client Rate"


@GameOptions_Factory_Register
class GameOption_UT99_NetServerMaxTickRate(GameOption_UT99):
    szOptionName = "NetServerMaxTickRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "NetServerMaxTickRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "60"
    szHelp = "Server Max TickRate"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("Engine.DemoRecDriver", "NetServerMaxTickRate", value)
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT99_LanServerMaxTickRate(GameOption_UT99):
    szOptionName = "LanServerMaxTickRate"
    szSectionName = "IpDrv.TcpNetDriver"
    szKeyName = "LanServerMaxTickRate"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "60"
    szHelp = "Lan Server Max TickRate"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("Engine.DemoRecDriver", "LanServerMaxTickRate", value)
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT99_AdminPassword(GameOption_UT99):
    szOptionName = "AdminPassword"
    szSectionName = "Engine.GameInfo"
    szKeyName = "AdminPassword"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "cfographut"
    szHelp = "Admin password"

    def set(self, value: str) -> None:
        super().set(value)
        self.inifile.setaddkeyvalue("UTServerAdmin.UTServerAdmin", "AdminPassword", value)
        self.inifile.writefile()

    def get(self) -> Union[str, list[str]]:
        try:
            return super().get()
        except KeyNotFoundError:
            return self.inifile.getkeyvalue(
                "UTServerAdmin.UTServerAdmin",
                "AdminPassword",
            )

        raise NotImplementedError("method not implemented")


@GameOptions_Factory_Register
class GameOption_UT99_GamePassword(GameOption_UT99):
    szOptionName = "GamePassword"
    szSectionName = "Engine.GameInfo"
    szKeyName = "GamePassword"
    TValueType = OptionType.OT_STRING
    szDefaultValue = ""
    szHelp = "Game password"


@GameOptions_Factory_Register
class GameOption_UT99_MaxPlayers(GameOption_UT99):
    szOptionName = "MaxPlayers"
    szSectionName = "Engine.GameInfo"
    szKeyName = "MaxPlayers"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Max Players"


@GameOptions_Factory_Register
class GameOption_UT99_MaxSpectators(GameOption_UT99):
    szOptionName = "MaxSpectators"
    szSectionName = "Engine.GameInfo"
    szKeyName = "MaxSpectators"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Max Spectators"


@GameOptions_Factory_Register
class GameOption_UT99_AS_TimeLimit(GameOption_UT99):
    szOptionName = "AS_TimeLimit"
    szSectionName = "Botpack.Assault"
    szKeyName = "TimeLimit"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Time Limit"


@GameOptions_Factory_Register
class GameOption_UT99_DOM_TimeLimit(GameOption_UT99):
    szOptionName = "DOM_TimeLimit"
    szSectionName = "Botpack.Domination"
    szKeyName = "TimeLimit"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Time Limit"


@GameOptions_Factory_Register
class GameOption_UT99_CTF_TimeLimit(GameOption_UT99):
    szOptionName = "CTF_TimeLimit"
    szSectionName = "Botpack.CTFGame"
    szKeyName = "TimeLimit"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "20"
    szHelp = "Game Time Limit"


@GameOptions_Factory_Register
class GameOption_UT99_DM_TimeLimit(GameOption_UT99):
    szOptionName = "DM_TimeLimit"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "TimeLimit"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "10"
    szHelp = "Game Time Limit"


@GameOptions_Factory_Register
class GameOption_UT99_GoalTeamScore(GameOption_UT99):
    szOptionName = "GoalTeamScore"
    szSectionName = "Botpack.TeamGamePlus"
    szKeyName = "GoalTeamScore"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "3"
    szHelp = "Game Score Limit"


@GameOptions_Factory_Register
class GameOption_UT99_MaxTeamSize(GameOption_UT99):
    szOptionName = "MaxTeamSize"
    szSectionName = "Botpack.TeamGamePlus"
    szKeyName = "MaxTeamSize"
    TValueType = OptionType.OT_FLOAT
    szDefaultValue = "12"
    szHelp = "Maximum Team Size"


@GameOptions_Factory_Register
class GameOption_UT99_DM_FragLimit(GameOption_UT99):
    szOptionName = "DM_FragLimit"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "FragLimit"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "10"
    szHelp = "Game Score Limit"


@GameOptions_Factory_Register
class GameOption_UT99_ServerLogName(GameOption_UT99):
    szOptionName = "ServerLogName"
    szSectionName = "Engine.GameInfo"
    szKeyName = "ServerLogName"
    TValueType = OptionType.OT_STRING
    szDefaultValue = "server.log"
    szHelp = "Server Log Name"


@GameOptions_Factory_Register
class GameOption_UT99_WebServer(GameOption_UT99):
    szOptionName = "WebServer"
    szSectionName = "UWeb.WebServer"
    szKeyName = "ListenPort"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "8076"
    szHelp = "enable Web Server"

    def set(self, value: str) -> None:
        # fix ut99 v469c
        try:
            self.inifile.delkey("UWeb.WebServer", "Listenport")
        except KeyNotFoundError:
            pass
        super().set(value)
        if int(value) > 0:
            self.inifile.setaddkeyvalue("UWeb.WebServer", "bEnabled", "True")
        else:
            self.inifile.setaddkeyvalue("UWeb.WebServer", "bEnabled", "False")
        self.inifile.writefile()


@GameOptions_Factory_Register
class GameOption_UT99_TournamentMode(GameOption_UT99):
    szOptionName = "TournamentMode"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "bTournament"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "False"
    szHelp = "Enable Tournament Mode"


@GameOptions_Factory_Register
class GameOption_UT99_InitialBots(GameOption_UT99):
    szOptionName = "InitialBots"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "InitialBots"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "0"
    szHelp = "Initial Bots number"


@GameOptions_Factory_Register
class GameOption_UT99_MinPlayers(GameOption_UT99):
    szOptionName = "MinPlayers"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "MinPlayers"
    TValueType = OptionType.OT_INTEGER
    szDefaultValue = "0"
    szHelp = "Minimum player count (allow to adjust bots)"


@GameOptions_Factory_Register
class GameOption_UT99_AS_UseTranslocator(GameOption_UT99):
    szOptionName = "AS_UseTranslocator"
    szSectionName = "Botpack.CTFGame"
    szKeyName = "bUseTranslocator"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Enable Translocator"


@GameOptions_Factory_Register
class GameOption_UT99_CTF_UseTranslocator(GameOption_UT99):
    szOptionName = "CTF_UseTranslocator"
    szSectionName = "Botpack.CTFGame"
    szKeyName = "bUseTranslocator"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Enable Translocator"


@GameOptions_Factory_Register
class GameOption_UT99_DM_UseTranslocator(GameOption_UT99):
    szOptionName = "DM_UseTranslocator"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "bUseTranslocator"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Enable Translocator"


@GameOptions_Factory_Register
class GameOption_UT99_DOM_UseTranslocator(GameOption_UT99):
    szOptionName = "DOM_UseTranslocator"
    szSectionName = "Botpack.Domination"
    szKeyName = "bUseTranslocator"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Enable Translocator"


@GameOptions_Factory_Register
class GameOption_UT99_CTF_ForceRespawn(GameOption_UT99):
    szOptionName = "CTF_ForceRespawn"
    szSectionName = "Botpack.CTFGame"
    szKeyName = "bForceRespawn"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Force Player to respawn"


@GameOptions_Factory_Register
class GameOption_UT99_DM_ForceRespawn(GameOption_UT99):
    szOptionName = "DM_ForceRespawn"
    szSectionName = "Botpack.DeathMatchPlus"
    szKeyName = "bForceRespawn"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Force Player to respawn"


@GameOptions_Factory_Register
class GameOption_UT99_DOM_ForceRespawn(GameOption_UT99):
    szOptionName = "DOM_ForceRespawn"
    szSectionName = "Botpack.Domination"
    szKeyName = "bForceRespawn"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Force Player to respawn"


@GameOptions_Factory_Register
class GameOption_UT99_AS_ForceRespawn(GameOption_UT99):
    szOptionName = "AS_ForceRespawn"
    szSectionName = "Botpack.Assault"
    szKeyName = "bForceRespawn"
    TValueType = OptionType.OT_BOOLEAN
    szDefaultValue = "True"
    szHelp = "Force Player to respawn"
