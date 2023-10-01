#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyGameCFG(c) by chacha
#
# pyGameCFG  is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""CLI interface module"""
from __future__ import annotations
from typing import Literal, cast, Union

import sys
from tap import Tap

from . import __Summuary__, __Name__
from . import GameOptions_Factory


class pygamecfg_args_SetOption(Tap):
    """SetOption CLI arg subparser"""

    option: str
    value: str = ""

    def configure(self) -> None:
        self.add_argument("option")
        self.add_argument("value")


class pygamecfg_args_RemOption(Tap):
    """RemOption CLI arg subparser"""

    option: str
    value: str = ""

    def configure(self) -> None:
        self.add_argument("option")
        self.add_argument("value")


class pygamecfg_args_GetOption(Tap):
    """GetOption CLI arg subparser"""

    option: str

    def configure(self) -> None:
        self.add_argument("option")


class pygamecfg_args(Tap):
    """Main CLI arg parser"""

    verbosity: int = 0
    basegamedir: str = "./"
    configfile: str = ""
    game: Literal["ut99", "cod4", "cod4_gungame", "cod4_promod", "ut2k4"]

    def configure(self) -> None:
        self.add_argument("-v", "--verbosity", action="count", help="increase output verbosity")
        self.add_argument("-b", "--basegamedir", help="set the game base dir")
        self.add_argument("-c", "--configfile", help="set the default config file")
        self.add_argument("-g", "--game", help="the target game")
        self.add_subparsers(dest="command", help="command type", required=True)
        self.add_subparser("SetOption", pygamecfg_args_SetOption, help="Set/Add a game config file option value")
        self.add_subparser("RemOption", pygamecfg_args_RemOption, help="Remove a game config file option, w or w/o value")
        self.add_subparser("GetOption", pygamecfg_args_GetOption, help="Get a game config file option value")

    def process_args(self) -> None:
        """dynamically add self.command to avoid conflict with Tap/argparse while keep pylint happy"""
        self.command: Union[str, None] = cast(Union[str, None], self.command)  # pylint: disable=attribute-defined-outside-init


def fct_main(i_args: list[str]) -> None:
    """CLI main function"""
    parser: pygamecfg_args = pygamecfg_args(prog=__Name__, description=__Summuary__)

    args: pygamecfg_args = parser.parse_args(i_args)

    if args.verbosity:
        print(f"Using base game dir: {args.basegamedir}")
        print(f"Using config file: {args.configfile}")

    if args.configfile == "":
        if args.game == "ut99":
            args.configfile = "./System/UnrealTournament.ini"
        if args.game == "ut2k4":
            args.configfile = "./System/UT2004.ini"
        elif args.game in ("cod4", "cod4_gungame", "cod4_promod"):
            args.configfile = "./main/server.cfg"

    GameOptions = GameOptions_Factory(args.game, args.basegamedir, args.configfile)
    if args.command == "SetOption":
        GameOptions.set(
            cast(pygamecfg_args_SetOption, args).option, cast(pygamecfg_args_SetOption, args).value  # pylint: disable=no-member
        )
    elif args.command == "RemOption":
        GameOptions.rem(
            cast(pygamecfg_args_RemOption, args).option, cast(pygamecfg_args_RemOption, args).value  # pylint: disable=no-member
        )
    elif args.command == "GetOption":
        res = GameOptions.get(cast(pygamecfg_args_GetOption, args).option)  # pylint: disable=no-member
        print(res)
    else:
        raise RuntimeError("Invalid argument")


if __name__ == "__main__":
    fct_main(sys.argv[1:])
