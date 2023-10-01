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


class GameOption_COD4_ProMod(GameOption_COD4):
    szGameType = "cod4_promod"


@GameOptions_Factory_Register
class GameOption_COD4_ProMod_promod_mode(GameOption_COD4_ProMod):
    TValueType = OptionType.OT_STRING
    szOptionName: str = "promod_mode"
    szKeyName: str = "promod_mode"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "comp_public"
    szHelp = """comp_public,custom_public,2v2_mr,1v1_mr,knockout_mr,match_mr"""


@GameOptions_Factory_Register
class GameOption_COD4_ProMod_promod_enable_scorebot(GameOption_COD4_ProMod):
    TValueType = OptionType.OT_BOOLEAN
    szOptionName: str = "promod_enable_scorebot"
    szKeyName: str = "promod_enable_scorebot"
    bDblQuoted: bool = True
    szPrefix = "set"
    szDefaultValue = "0"
    szHelp = """match-modes only"""
