#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

# pylint: disable=missing-class-docstring,missing-module-docstring,missing-function-docstring,duplicate-code,line-too-long
from __future__ import annotations
from typing import Union

import re
from os.path import join
from os import linesep

from .core_gamecfg import GameOptions_Factory_Register, GameOption, OptionType, GameCfgException


class COD4KeyNotFoundError(GameCfgException):
    """Exception to catch non existing configuration key in COD4 configuration file"""


class GameOption_COD4(GameOption):
    szGameType = "cod4"
    TValueType = OptionType.OT_INVALID

    szOptionName: str = ""
    szKeyName: str = ""
    bDblQuoted: bool = False
    szPrefix: str = ""

    def __init__(self, GameRootDir: str, ConfigFileRelPath: str) -> None:
        super().__init__(GameRootDir, ConfigFileRelPath)
        self.mainConfigFilePath = join(GameRootDir, ConfigFileRelPath)
        self.cfgfile = open(self.mainConfigFilePath, "r", encoding="utf8")  # pylint: disable=consider-using-with

    def format_OT_BOOLEAN(self, value: Union[int, str, float]) -> str:
        return "1" if super().format_OT_BOOLEAN(value).lower() == "true" else "0"

    def close(self) -> None:
        self.cfgfile.close()

    def set(self, value: str) -> None:
        if not self.szOptionName:
            raise RuntimeError("szOptionName is not set")

        FinalValue: str = value
        if self.bDblQuoted:
            FinalValue = '"' + FinalValue + '"'
        if self.szPrefix != "":
            FinalValue = self.szPrefix + " " + self.szKeyName + " " + FinalValue + linesep
        bfound = False
        newFile = ""

        regex = r"^\s*" + self.szPrefix + r"\s+" + self.szKeyName + r"\s*(?P<value>.*)"

        for line in self.cfgfile.readlines():
            if re.search(regex, line):
                if bfound:
                    print("[warning] Option defined multiple time")
                newFile += FinalValue
                bfound = True
            else:
                newFile += line

        if not bfound:
            # write new key at the top of the file to be sure we do not erase the map / map_rotate cmd
            newFile = FinalValue + newFile

        self.cfgfile.close()
        with open(self.mainConfigFilePath, "w", encoding="utf8") as ofile:
            ofile.write(newFile)
        self.cfgfile = open(self.mainConfigFilePath, "r", encoding="utf8")  # pylint: disable=consider-using-with

    def rem(self, value: Union[str, None] = None) -> None:
        if not self.szOptionName:
            raise RuntimeError("szOptionName is not set")

        regex = r"^\s*" + self.szPrefix + r"\s+" + self.szKeyName + r"\s*(?P<value>.*)"

        bfound = False
        newFile = ""
        for line in self.cfgfile.readlines():
            if re.search(regex, line):
                if bfound:
                    print("[warning] Option defined multiple time")
                bfound = True
            else:
                newFile += line
        if not bfound:
            raise COD4KeyNotFoundError("Option not found in file")

        self.cfgfile.close()
        with open(self.mainConfigFilePath, "w", encoding="utf8") as ofile:
            ofile.write(newFile)
        self.cfgfile = open(self.mainConfigFilePath, "r", encoding="utf8")  # pylint: disable=consider-using-with

    def get(self) -> str:
        if not self.szOptionName:
            raise RuntimeError("szOptionName not set")

        if self.bDblQuoted:
            regex = r"^\s*" + self.szPrefix + r"\s+" + self.szKeyName + r"\s*\"(?P<value>.*)\""
        else:
            regex = r"^\s*" + self.szPrefix + r"\s+" + self.szKeyName + r"\s*(?P<value>.*)"
        bfound = False

        for line in self.cfgfile.readlines():
            if result := re.search(regex, line):
                if bfound:
                    raise RuntimeError("Option defined multiple time")
                res = result.groupdict()["value"]
                bfound = True
        if not bfound:
            raise COD4KeyNotFoundError("Option not found in file")
        return res


@GameOptions_Factory_Register
class GameOption_COD4_Meta_Admin(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "meta_admin"
    szKeyName: str = "_Admin"
    bDblQuoted: bool = True
    szPrefix = "sets"
    szDefaultValue = "ServAdmin"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_Meta_Email(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "meta_email"
    szKeyName: str = "_Email"
    bDblQuoted: bool = True
    szPrefix = "sets"
    szDefaultValue = "ServEmail"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_Meta_Website(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "meta_website"
    szKeyName: str = "_Website"
    bDblQuoted: bool = True
    szPrefix = "sets"
    szDefaultValue = "ServWebsite"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_Meta_Location(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "meta_location"
    szKeyName: str = "_Location"
    bDblQuoted: bool = True
    szPrefix = "sets"
    szDefaultValue = "ServLocation"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_Meta_Maps(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "meta_maps"
    szKeyName: str = "_Maps"
    bDblQuoted: bool = True
    szPrefix = "sets"
    szDefaultValue = ""
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_Meta_Gametype(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "meta_gametype"
    szKeyName: str = "_Gametype"
    bDblQuoted: bool = True
    szPrefix = "sets"
    szDefaultValue = ""
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_Cod4x_AuthToken(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "cod4x_authtoken"
    szKeyName: str = "sv_authtoken"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = "Cod4x personnal auth token"


@GameOptions_Factory_Register
class GameOption_COD4_Hostname(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "hostname"
    szKeyName: str = "sv_hostname"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = "Server Hostname"


@GameOptions_Factory_Register
class GameOption_COD4_MOTD(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "motd"
    szKeyName: str = "g_motd"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "Welcome"
    szHelp = "Server Message Of The Day"


@GameOptions_Factory_Register
class GameOption_COD4_dedicated(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dedicated"
    szKeyName: str = "dedicated"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "2"
    szHelp = """0 = Listen, 1 = LAN, 2 = Internet ( you probably want 2 )"""


@GameOptions_Factory_Register
class GameOption_COD4_RCON_password(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "rcon_password"
    szKeyName: str = "rcon_password"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = "password for remote access, leave empty to deactivate, min 8 characters"


@GameOptions_Factory_Register
class GameOption_COD4_game_password(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "game_password"
    szKeyName: str = "g_password"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = "join password, leave empty to deactivate"


@GameOptions_Factory_Register
class GameOption_COD4_nb_private_clients(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "nb_privateClients"
    szKeyName: str = "sv_privateClients"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "3"
    szHelp = """Private Clients, number of slots that can only be changed with a password"""


@GameOptions_Factory_Register
class GameOption_COD4_private_password(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "private_password"
    szKeyName: str = "sv_privatePassword"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = "the password to join private slots"


@GameOptions_Factory_Register
class GameOption_COD4_maxclients(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "maxclients"
    szKeyName: str = "sv_maxclients"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "12"
    szHelp = """Maximum client number"""


@GameOptions_Factory_Register
class GameOption_COD4_logsync(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "logsync"
    szKeyName: str = "g_logsync"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "2"
    szHelp = """0=no log, 1=buffered, 2=continuous, 3=append"""


@GameOptions_Factory_Register
class GameOption_COD4_enable_logfile(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "enable_logfile"
    szKeyName: str = "logfile"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """0 = NO log, 1 = log file enabled"""


@GameOptions_Factory_Register
class GameOption_COD4_logfile(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "logfile"
    szKeyName: str = "g_log"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "games_mp.log"
    szHelp = "Name of log file, default is games_mp.log"


@GameOptions_Factory_Register
class GameOption_COD4_enable_logdamage(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "enable_logdamage"
    szKeyName: str = "sv_log_damage"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """0 = NO logdamage, 1 = logdamage enabled"""


@GameOptions_Factory_Register
class GameOption_COD4_statusfile(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "statusfile"
    szKeyName: str = "sv_statusfile"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "serverstatus.xml"
    szHelp = "writes an xml serverstatus to disc, leave empty to disable"


@GameOptions_Factory_Register
class GameOption_COD4_ney_port(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "net_port"
    szKeyName: str = "net_port"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "28960"
    szHelp = """network port"""


@GameOptions_Factory_Register
class GameOption_COD4_maxRate(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "maxRate"
    szKeyName: str = "sv_maxRate"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "25000"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_minPing(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "minPing"
    szKeyName: str = "sv_minPing"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = "minimal ping [ms] for a player to join the server"


@GameOptions_Factory_Register
class GameOption_COD4_maxPing(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "maxPing"
    szKeyName: str = "sv_maxPing"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "350"
    szHelp = "maximal ping [ms] for a player to join the server"


@GameOptions_Factory_Register
class GameOption_COD4_randomMapRotation(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "randomMapRotation"
    szKeyName: str = "sv_randomMapRotation"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """0 = sv_mapRotation is randomized, 1 = sequential order of sv_mapRotation"""


@GameOptions_Factory_Register
class GameOption_COD4_teambalance(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "teambalance"
    szKeyName: str = "scr_teambalance"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = "auto-teambalance //0 = no, 1 = yes"


@GameOptions_Factory_Register
class GameOption_COD4_team_fftype(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "team_fftype"
    szKeyName: str = "scr_team_fftype"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = "friendly-fire //0 = off, 1 = on, //2 = reflect damage, 3 = shared damage"


@GameOptions_Factory_Register
class GameOption_COD4_enable_hardcore(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "hardcore"
    szKeyName: str = "scr_hardcore"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """Hardcore Mode //0 = off 1 = on"""


@GameOptions_Factory_Register
class GameOption_COD4_enable_oldschool(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "oldschool"
    szKeyName: str = "scr_oldschool"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """Oldschool Mode //0 = off, 1 = on"""


@GameOptions_Factory_Register
class GameOption_COD4_enable_friendlyPlayerCanBlock(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "friendlyPlayerCanBlock"
    szKeyName: str = "g_friendlyPlayerCanBlock"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """1 = player collision between friendly players, 0 = collision between friendly players is disabled"""


@GameOptions_Factory_Register
class GameOption_COD4_enable_FFAPlayerCanBlock(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "FFAPlayerCanBlock"
    szKeyName: str = "g_FFAPlayerCanBlock"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """1 = player collision, 0 = collision between players is disabled"""


@GameOptions_Factory_Register
class GameOption_COD4_DM_scorelimit(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dm_scorelimit"
    szKeyName: str = "scr_dm_scorelimit"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1000"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_DM_timelimit(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dm_timelimit"
    szKeyName: str = "scr_dm_timelimit"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "15"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_DM_roundlimit(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dm_roundlimit"
    szKeyName: str = "scr_dm_roundlimit"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_DM_numlives(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dm_numlives"
    szKeyName: str = "scr_dm_numlives"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_DM_playerrespawndelay(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dm_playerrespawndelay"
    szKeyName: str = "scr_dm_playerrespawndelay"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_DM_waverespawndelay(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "dm_waverespawndelay"
    szKeyName: str = "scr_dm_waverespawndelay"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_TDM_scorelimit(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "tdm_scorelimit"
    szKeyName: str = "scr_war_scorelimit"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "2000"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_TDM_timelimit(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "tdm_timelimit"
    szKeyName: str = "scr_war_timelimit"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "10"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_TDM_roundlimit(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "tdm_roundlimit"
    szKeyName: str = "scr_war_roundlimit"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_TDM_numlives(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "tdm_numlives"
    szKeyName: str = "scr_war_numlives"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_TDM_playerrespawndelay(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "tdm_playerrespawndelay"
    szKeyName: str = "scr_war_playerrespawndelay"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_TDM_waverespawndelay(GameOption_COD4):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "tdm_waverespawndelay"
    szKeyName: str = "scr_war_waverespawndelay"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_gametype(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "gametype"
    szKeyName: str = "g_gametype"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "dm"
    szHelp = "gamemode, one of [war, dm, sd, sab, koth]"


@GameOptions_Factory_Register
class GameOption_COD4_mapRotation(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mapRotation"
    szKeyName: str = "sv_mapRotation"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "gametype dm map mp_block"
    szHelp = """Map rotation list"""


@GameOptions_Factory_Register
class GameOption_COD4_allowdownloadk(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "allowdownload"
    szKeyName: str = "sv_allowdownload"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_wwwDownload(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "wwwDownload"
    szKeyName: str = "sv_wwwDownload"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_wwwBaseURL(GameOption_COD4):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "wwwBaseURL"
    szKeyName: str = "sv_wwwBaseURL"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_wwwDlDisconnected(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "wwwDlDisconnected"
    szKeyName: str = "sv_wwwDlDisconnected"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = ""


@GameOptions_Factory_Register
class GameOption_COD4_nosteamnames(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "nosteamnames"
    szKeyName: str = "sv_nosteamnames"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = "1 = Use names from steam if steam is available"


@GameOptions_Factory_Register
class GameOption_COD4_punkbuster(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "punkbuster"
    szKeyName: str = "sv_punkbuster"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = "Enable Punkbuste (PB is not supported on CoD4x)"


@GameOptions_Factory_Register
class GameOption_COD4_pure(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "pure"
    szKeyName: str = "sv_pure"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = "check IWD-data 0 = off, 1 = on"


@GameOptions_Factory_Register
class GameOption_COD4_antilag(GameOption_COD4):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "antilag"
    szKeyName: str = "g_antilag"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = "0 = off, 1 = on // Anti lag checks for weapon hits"
