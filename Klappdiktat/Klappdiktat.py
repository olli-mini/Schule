#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set autoindent smartindent softtabstop=4 tabstop=4 shiftwidth=4 expandtab:
from __future__ import (
    print_function,
    with_statement,
    unicode_literals,
    division,
    absolute_import,
)

__author__ = "Oliver Schneider"
__copyright__ = "2024 Oliver Schneider (assarbad.net), under the terms of the UNLICENSE"
__version__ = "0.1"
__compatible__ = ((3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3,13))  # fmt: skip
__doc__ = """
===============================
 Klappdiktat
===============================
"""
import argparse

import os

# import re
import sys

# from contextlib import suppress
# from copy import deepcopy
from functools import partial  # also cache
from pathlib import Path

# from pprint import pformat, pprint
# from typing import Optional

eprint = partial(print, file=sys.stderr)

# Checking for compatibility with Python version
if not sys.version_info[:2] in __compatible__:
    sys.exit(
        f"This script is only compatible with the following Python versions: {', '.join([f'{z[0]}.{z[1]}' for z in __compatible__])}"
    )  # pragma: no cover

CONFIG_DEFAULTS = """
[foobar]
baz = %(thisdir)s/bla.txt
"""


def parse_options() -> argparse.Namespace:
    """\
        Initializes the ArgumentParser and ConfigParser and performs the parsing
    """
    from argparse import ArgumentParser
    from configparser import ConfigParser
    from textwrap import dedent

    cfgname = Path(__file__).absolute().with_suffix(".ini")
    cfg = ConfigParser(defaults={"thisdir": cfgname.parent}, delimiters=("=",))
    cfg.read_string(dedent(CONFIG_DEFAULTS), "<DEFAULTS>")
    parser = ArgumentParser(
        description="Kleines Programm um LaTeX-Schnipsel für Klappdiktat zu erzeugen",
        add_help=False,
    )
    # Only add the configuration file argument for starters
    parser.add_argument(
        "-c",
        "--config",
        "--ini",
        action="store",
        default=cfgname,
        metavar="CFG",
        type=Path,
        help=f"The config file; defaults to {cfgname}",
    )
    partial_args = parser.parse_known_args()[0]
    cfg.read(partial_args.config)

    # Remaining command line options
    parser.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    parser.add_argument(
        "--nologo",
        action="store_const",
        dest="nologo",
        const=True,
        help="Don't show info about this script.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Turn up verbosity to see more details of what is going on.",
    )
    parser.add_argument("file", nargs="+")
    return cfg, parser.parse_args()


def single_file(wortliste):
    print(f"{wortliste=}")
    worte = []
    wortgruppe = []
    with open(wortliste) as liste:
        while line := liste.readline():
            if line.startswith("#"):
                if wortgruppe:
                    worte.append(wortgruppe)  ## ja, verschachtelt
                wortgruppe = []
                continue
            wortgruppe = wortgruppe + [x.strip() for x in line.strip().split(",")]
    if wortgruppe:
        worte.append(wortgruppe)  # letzte Gruppe
    counter = 0
    ausgabe = Path(wortliste).with_suffix(".tex")
    with open(ausgabe, "w") as wortinc:
        for wortgruppe in worte:
            counter += 1
            print(f"""%% Neue Wortgruppe""", file=wortinc)
            print(
                """\t\\begin{tblr}{\n\t\tcolspec={X[10,t]|[dashed]X[40,t]},\n\t}""",
                file=wortinc,
            )
            for wort in wortgruppe:
                print(
                    f"""\t\t{{\\prima {wort}}} & {{\\grundschrift{{\\strut}}}} \\\\""",
                    file=wortinc,
                )
            print("""\t\\end{tblr}""", file=wortinc)
            if counter > 0:
                break


def main() -> int:
    """\
        Very simply the main entry point to this script
    """
    verzeichnis = os.path.dirname(os.path.realpath(__file__))
    for liste in args.file:
        single_file(liste)
    return 0


if __name__ == "__main__":
    global args
    global cfg
    cfg, args = parse_options()
    try:
        sys.exit(main())
    except SystemExit:
        pass
    except ImportError:
        raise  # re-raise
    except RuntimeError:
        raise  # re-raise
    except Exception:
        eprint(__doc__)
        raise  # re-raise
