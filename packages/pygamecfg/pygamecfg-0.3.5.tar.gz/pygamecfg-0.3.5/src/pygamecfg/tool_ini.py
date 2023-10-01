#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""utility module that contain PySimpleINI based helpers"""
from __future__ import annotations
from typing import Union
from pysimpleini import PySimpleINI, SectionNotFoundError, Key, Section


class PySimpleINI_GroupKeysInSection(PySimpleINI):
    """a class base on PySimpleINI that allow user to force some key to be group together in a section"""

    GroupRules: list[tuple[str, str]] = []

    def groupkeysinsection(self, szSectionName: str, szKeyName: str) -> None:
        """internal function that actually group keys"""
        try:
            _section: list[Section] = self.getsection(szSectionName)
            if len(_section) == 1:
                ar_ServerPackages: Union[list[Key], Key] = _section[0].getkey(szKeyName)
                if isinstance(ar_ServerPackages, Key):
                    ar_ServerPackages = [ar_ServerPackages]
                else:  # array
                    pass
                for ServerPackages in ar_ServerPackages:
                    _section[0].delkey(ServerPackages.getname(), None, ServerPackages.getvalue())
                for ServerPackages in ar_ServerPackages:
                    _section[0].setaddkeyvalue(ServerPackages.getname(), ServerPackages.getvalue(), True)
        except SectionNotFoundError:
            pass

    def writefile(self, bBeautify: bool = False, bWipeComments: bool = False) -> None:
        """overload of the write function to call the group function before"""
        for GroupRule in self.GroupRules:
            self.groupkeysinsection(GroupRule[0], GroupRule[1])
        super().writefile(bBeautify, bWipeComments)
