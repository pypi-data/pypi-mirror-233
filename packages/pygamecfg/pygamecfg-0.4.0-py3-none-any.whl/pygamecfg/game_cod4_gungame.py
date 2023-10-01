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

from .core_gamecfg import GameOptions_Factory_Register, OptionType
from .game_cod4 import GameOption_COD4


class GameOption_COD4_GunGame(GameOption_COD4):
    szGameType = "cod4_gungame"


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_kills_for_levelup(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "kills_for_levelup"
    szKeyName: str = "gg_kills_for_levelup"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "2"
    szHelp = """Number of kills you need to level-up"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_turbo(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "turbo"
    szKeyName: str = "gg_turbo"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Turbo Mode: Give the new weapon immediately"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_level_down(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "level_down"
    szKeyName: str = "gg_level_down"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Number of levels you lose on suicide, teamkill..."""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_health_regen_time(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "health_regen_time"
    szKeyName: str = "gg_health_regen_time"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "6"
    szHelp = """Time before health regeneration starts: 5 = default, 0 = disable health regen"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_health_text(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "health_text"
    szKeyName: str = "gg_health_text"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Text in the bottom-left part of the screen that shows your health"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_weapon_drop(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "weapon_drop"
    szKeyName: str = "gg_weapon_drop"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Drop weapons on death?"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_knife_nerf(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "knife_nerf"
    szKeyName: str = "gg_knife_nerf"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """0 = default, 1 = knife needs 2 hits to kill"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_dont_cook_frags(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "dont_cook_frags"
    szKeyName: str = "gg_dont_cook_frags"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """1 = don't cook frag grenades, 0 = default nades"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_end_music(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "end_music"
    szKeyName: str = "gg_end_music"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Music at the end of the map"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_knife_pro(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "knife_pro"
    szKeyName: str = "gg_knife_pro"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """When you knife someone you steal a level from him"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_deadly_snipers(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "deadly_snipers"
    szKeyName: str = "gg_deadly_snipers"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """1 = increase damage for bolt-action snipers, 2 = increase damage for all snipers"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_handicap(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "handicap"
    szKeyName: str = "gg_handicap"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """If a player joins in the middle of the game he is auto leveled to the level the worst player has"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_ammo_frag(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "ammo_frag"
    szKeyName: str = "gg_ammo_frag"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "6"
    szHelp = """Ammo for frag grenades [1-10]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_ammo_c4(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "ammo_c4"
    szKeyName: str = "gg_ammo_c4"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "4"
    szHelp = """Ammo for C4 [1-10]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_ammo_rpg(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "ammo_rpg"
    szKeyName: str = "gg_ammo_rpg"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "3"
    szHelp = """Ammo for RPG [1-10]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_rotate_empty(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "rotate_empty"
    szKeyName: str = "gg_rotate_empty"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "10"
    szHelp = """Minutes after which server rotates to next map if no active players"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_remove_turrets(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "remove_turrets"
    szKeyName: str = "gg_remove_turrets"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Remove stationary turrets [0=turrets allwed; 1=turrets removed]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_second_weapon(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "second_weapon"
    szKeyName: str = "gg_second_weapon"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "deserteagle"
    szHelp = """The second weapon the players will have (empty to disable)"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_second_weapon_levels(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "second_weapon_levels"
    szKeyName: str = "gg_second_weapon_levels"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "c4,rpg,frag_grenade,rpg"
    szHelp = """The second weapon the players will have (empty to disable)"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_weapon_sequence(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "weapon_sequence"
    szKeyName: str = "gg_weapon_sequence"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "beretta,usp,colt45,deserteagle,winchester1200,m1014,mp5,m40a3,skorpion,uzi,ak74u,p90,m16,ak47,m4,g3,g36c,m14,mp44,saw,rpd,m60e4,barett,remington700,rpg,frag_grenade,knife"
    szHelp = """comma separated list from: beretta,usp,colt45,deserteagle,winchester1200,m1014,mp5,skorpion,uzi,ak74u,p90,m16,ak47,m4,g3,g36c,m14,mp44,saw,rpd,m60e4,m40a3,m21,dragunov,remington700,barrett,frag_grenade,knife,c4,rpg"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Enable(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "mc_enable"
    szKeyName: str = "mc_enable"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """Enable rotating messages? [0: disable; 1: new custom messages; 2: standard print messages bottom left]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Delay(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "mc_delay"
    szKeyName: str = "mc_delay"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "20"
    szHelp = """Delay between messages (sec)"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_MaxMsg(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_INTEGER
    szOptionName: str = "mc_max_msg"
    szKeyName: str = "mc_max_msg"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """Maximum number of messages to use [max 20]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_0(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_0"
    szKeyName: str = "mc_msg_0"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 0 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_1(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_1"
    szKeyName: str = "mc_msg_1"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 1 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_2(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_2"
    szKeyName: str = "mc_msg_2"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 2 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_3(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_3"
    szKeyName: str = "mc_msg_3"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 3 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_4(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_4"
    szKeyName: str = "mc_msg_4"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 4 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_5(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_5"
    szKeyName: str = "mc_msg_5"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 5 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_MessageCenter_Message_6(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "mc_msg_6"
    szKeyName: str = "mc_msg_6"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = ""
    szHelp = """message num 6 in rotation"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_WelcomeMessage_Enable(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "wc_enable"
    szKeyName: str = "wc_enable"
    bDblQuoted: bool = False
    szPrefix = "set"
    szDefaultValue = "1"
    szHelp = """Enable welcome message"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_WelcomeMessage_Messsage(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "wc_message"
    szKeyName: str = "wc_message"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = r"Welcome to the server <name>!\Please enjoy your stay!"
    szHelp = r"""The message [ <name> is replaced by players name and \ indicates a new line ]"""


@GameOptions_Factory_Register
class GameOption_COD4_GunGame_bottom_text(GameOption_COD4_GunGame):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "bottom_text"
    szKeyName: str = "gg_bottom_text"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "GunGame Server"
    szHelp = """ Hud [ custom text displayed on the bottom of the screen next to mod info ]"""
