#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.
# pylint: disable=wrong-import-position
"""
Main module __init__ file.
"""

from importlib.metadata import distribution, version, PackageNotFoundError
import warnings


try:  # pragma: no cover
    __version__ = version("pygamecfg")
except PackageNotFoundError:  # pragma: no cover
    warnings.warn("can not read __version__, assuming local test context, setting it to ?.?.?")
    __version__ = "?.?.?"

try:  # pragma: no cover
    dist = distribution("pygamecfg")
    __Summuary__ = dist.metadata["Summary"]
except PackageNotFoundError:  # pragma: no cover
    warnings.warn('can not read dist.metadata["Summary"], assuming local test context, setting it to <pygamecfg description>')
    __Summuary__ = "pygamecfg description"

try:  # pragma: no cover
    dist = distribution("pygamecfg")
    __Name__ = dist.metadata["Name"]
except PackageNotFoundError:  # pragma: no cover
    warnings.warn('can not read dist.metadata["Name"], assuming local test context, setting it to <pygamecfg>')
    __Name__ = "pygamecfg"

from .core_gamecfg import GameOptions_Factory
from . import game_cod4
from . import game_cod4_gungame
from . import game_cod4_promod
from . import game_ut99
from . import game_ut2k4
