#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""common UT functions"""
from __future__ import annotations
from typing import Union

from os.path import join
from pathlib import Path

from pysimpleini import PySimpleINI

from .core_gamecfg import GameOption, OptionType


class GameOption_UT(GameOption):
    """generic UT Option class"""

    szGameType = ""
    TValueType = OptionType.OT_INVALID

    szOptionName = ""
    szSectionName = ""
    szKeyName = ""
    bForceAdd: bool = False
    bRemovable: bool = False

    cachedFile: Union[None, PySimpleINI] = None
    cachedFilePath: Union[None, Path] = None

    Cls_PySimpleINI: type[PySimpleINI] = PySimpleINI

    @classmethod
    def openFile(cls, filepath: Path) -> PySimpleINI:
        """Open the file"""
        if (not cls.cachedFile) or (filepath != cls.cachedFilePath):
            cls.cachedFilePath = filepath
            cls.cachedFile = cls.Cls_PySimpleINI(filepath)
        return cls.cachedFile

    def __init__(self, GameRootDir: str, ConfigFileRelPath: str) -> None:
        super().__init__(GameRootDir, ConfigFileRelPath)
        self.mainConfigFilePath: Path = Path(join(GameRootDir, ConfigFileRelPath))
        self.inifile = self.openFile(self.mainConfigFilePath)

    def set(self, value: str) -> None:
        if not self.szOptionName:
            raise RuntimeError("szOptionName is not set")
        self.format(value)
        self.inifile.setaddkeyvalue(self.szSectionName, self.szKeyName, value, self.bForceAdd)
        self.inifile.writefile()

    def rem(self, value: Union[None, str]) -> None:
        if not self.szOptionName:
            raise RuntimeError("szOptionName is not set")
        if not self.bRemovable:
            raise RuntimeError("this options is not removable")
        self.inifile.delkey_ex(self.szSectionName, self.szKeyName, None, value)
        self.inifile.writefile()

    def get(self) -> Union[str, list[str]]:
        if not self.szOptionName:
            raise RuntimeError("szOptionName not set")
        return self.inifile.getkeyvalue(self.szSectionName, self.szKeyName)
