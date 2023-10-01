#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

""" Core file of pygamecfg
contain generic management code for GameOption
"""
from __future__ import annotations
from typing import Union

from abc import ABCMeta, abstractmethod
from enum import Enum


class GameCfgException(Exception):
    """Standard Exception to catch non existing key in configuration file"""


class OptionNotFoundError(GameCfgException):
    """Standard Exception to catch non existing configuration option"""


class OptionType(Enum):
    """Supported option data type"""

    OT_INVALID = 0
    OT_STRING = 1
    OT_INTEGER = 2
    OT_BOOLEAN = 3
    OT_FLOAT = 4


class GameOption(metaclass=ABCMeta):
    """Game option base type"""

    szGameType: str = ""
    szOptionName: str = ""
    TValueType: OptionType = OptionType.OT_INVALID
    szDefaultValue: str = ""
    szHelp: str = ""

    def __init__(self, GameRootDir: str, ConfigFileRelPath: Union[None, str] = None):
        """GameOption constructor.

        ///warning
        This object does not aim to be created
        ///

        Args:
            GameRootDir: root dir of the game
            ConfigFileRelPath: path to the configfile (relative to rootdir)
        """
        self.GameRootDir = GameRootDir
        self.ConfigFileRelPath = ConfigFileRelPath

    def __enter__(self) -> GameOption:
        """contextlib enter hook"""
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> None:
        """contextlib exit hook"""
        self.close()

    def close(self) -> None:
        """user-define close() function (for subclassing)"""

    def format_OT_STRING(self, value: Union[int, str, float]) -> str:
        """ "STRING specific format method (TO file)"""
        return str(value)

    def format_OT_INTEGER(self, value: Union[int, str, float]) -> str:
        """ "INTEGER specific format method (TO file)"""
        return str(int(value))

    def format_OT_BOOLEAN(self, value: Union[int, str, float]) -> str:
        """ "BOOLEAN specific format method (TO file)"""
        try:
            intval = int(value)
            return str(bool(intval))
        except ValueError:
            return str(True) if str(value).lower() == "true" else str(False)

    def format_OT_FLOAT(self, value: Union[int, str, float]) -> str:
        """ "FLOAT specific format method (TO file)"""
        return str(float(value))

    def format(self, value: Union[int, str, float]) -> str:
        """standard method to format options before writing it TO file (overloadable)"""

        FormatedValue: str = ""
        if self.TValueType == OptionType.OT_STRING:
            FormatedValue = self.format_OT_STRING(value)
        elif self.TValueType == OptionType.OT_INTEGER:
            FormatedValue = self.format_OT_INTEGER(value)
        elif self.TValueType == OptionType.OT_BOOLEAN:
            FormatedValue = self.format_OT_BOOLEAN(value)
        elif self.TValueType == OptionType.OT_FLOAT:
            FormatedValue = self.format_OT_FLOAT(value)
        else:
            raise RuntimeError("Invalid Option TValueType")

        print(f"setting option <{self.szOptionName}>  to:  {FormatedValue}")
        return FormatedValue

    @abstractmethod
    def set(self, value: str) -> None:
        """generic set function"""
        raise NotImplementedError("method not implemented")

    @abstractmethod
    def rem(self, value: Union[None, str]) -> None:
        """generic rem function"""
        raise NotImplementedError("method not implemented")

    @abstractmethod
    def get(self) -> Union[str, list[str]]:
        """generic get function"""
        raise NotImplementedError("method not implemented")


class GameOptions_Factory:
    """factory that manage game options based on Game and the option itself"""

    ar_Options_cls: list[type[GameOption]] = []
    ar_Options_cls_filtered: list[type[GameOption]] = []
    GameRootDir: str = "./"
    ConfigFileRelPath: str = ""

    def __init__(self, szGameType: str, GameRootDir: str, ConfigFileRelPath: str) -> None:
        self.szGameType = szGameType
        self.GameRootDir = GameRootDir
        self.ConfigFileRelPath = ConfigFileRelPath
        for Options_cls in GameOptions_Factory.ar_Options_cls:
            if Options_cls.szGameType == szGameType:
                self.ar_Options_cls_filtered.append(Options_cls)

    @classmethod
    def GameOptionRegister(cls, Option: type[GameOption]) -> None:
        """interface option used by decorator to register option implementation classes"""
        GameOptions_Factory.ar_Options_cls.append(Option)

    def set(self, OptionName: str, value: str) -> None:
        """generic set function (API call)"""
        for _option in GameOptions_Factory.ar_Options_cls_filtered:
            if _option.szOptionName == OptionName:
                with _option(self.GameRootDir, self.ConfigFileRelPath) as _optionInst:
                    _optionInst.set(_optionInst.format(value))
                return
        raise OptionNotFoundError("Option not found")

    def rem(self, OptionName: str, value: Union[None, str]) -> None:
        """generic rem function (API call)"""
        for _option in self.ar_Options_cls_filtered:
            if _option.szOptionName == OptionName:
                with _option(self.GameRootDir, self.ConfigFileRelPath) as _optionInst:
                    _optionInst.rem(value)
                return
        raise OptionNotFoundError("Option not found")

    def get(self, OptionName: str) -> Union[str, list[str]]:
        """generic get function (API call)"""
        for _option in self.ar_Options_cls_filtered:
            if _option.szOptionName == OptionName:
                with _option(self.GameRootDir, self.ConfigFileRelPath) as _optionInst:
                    return _optionInst.get()
        raise OptionNotFoundError("Option not found")


def GameOptions_Factory_Register(cls: type[GameOption]) -> type[GameOption]:
    """decorator to register game option concrete implementation"""
    GameOptions_Factory.GameOptionRegister(cls)
    return cls
