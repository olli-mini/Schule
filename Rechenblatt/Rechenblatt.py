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
import random
import sys

from functools import partial  # also cache
from pathlib import Path
from typing import Optional, Tuple, List

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
        description="Kleines Programm um LaTeX-Schnipsel für Rechenblätter zu erzeugen",
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
    return cfg, parser.parse_args()

def op_choice(x):
    retval = random.choice(x)
    assert len(retval) == 1, "Erwarte _eine_ Operation zurück"
    assert retval in {"+", "-", "*", "/"}, "Nur diese Operationen sind erlaubt"
    return retval

def aufgaben_mix(anzahl: int = 30, bereich: Tuple[int, int] = (1, 100), max_ergebnis: int = 100, operationen: int = 1, ops: str = "+-*/", positiv: bool = True):
    """\
    Erzeugt Aufgaben für Addition/Subtraktion/Multiplikation/Division mit bis zu vier Operanden
    """
    max_ergebnis = max_ergebnis or bereich[1]
    randint = random.randint
    assert operationen < 4, "Darf die Anzahl von vier Operationen nicht überschreiten, ansonsten muß das Tupel 'operanden' angepaßt werden"
    aufg_liste = []
    while len(aufg_liste) < anzahl:
        operanden = (randint(*bereich), randint(*bereich), randint(*bereich), randint(*bereich))
        if operanden[0] == operanden[1]:
            continue
        if operationen > 1 and operanden[1] == operanden[2]:
            continue
        if operationen < 2 and (operanden[0] in {1} or operanden[1] in {1, 2}):
            continue
        aufgabe = f"{operanden[0]} {op_choice(ops)} {operanden[1]}"
        if "/" in aufgabe: # Extra-Bedingung für Division ... nur ganze Zahlen!
            remainder = eval(aufgabe.replace("/", "%"))
            if remainder != 0:
                continue
        res = eval(aufgabe)
        if positiv and (res < 0):
            continue
        if operationen >= 2:
            aufgabe = f"{aufgabe} {op_choice(ops)} {operanden[2]}"
        res = eval(aufgabe)
        if positiv and (res < 0):
            continue
        if operationen >= 3:
            aufgabe = f"{aufgabe} {op_choice(ops)} {operanden[3]}"
        res = eval(aufgabe)
        if res > max_ergebnis:
            continue
        if positiv and (res < 0):
            continue
        if aufgabe not in aufg_liste:
            aufg_liste.append(aufgabe)
    return aufg_liste

def op_filter(aufgabe):
    return aufgabe.replace("*", "$\\cdot$").replace("/", "$\\div$")

def schreib_aufgaben(datei: str, aufgaben: List[str]):
    with open(datei, "w") as ausgabe:
        print(f"Schreibe: {datei}", file=sys.stderr)
        print("\t\\begin{mdframed}[style=Rechnen]\n\t\t\\begin{tblr}{\n\t\t\tcolspec={X[3,r]X[2,l]X[3,r]X[2,l]X[3,r]X[2,l]},\n\t\t\twidth=\\textwidth,\n\t\t\trowsep=1pt,\n\t\t\t}", file=ausgabe)
        for aufgabe in [aufgaben[i:i+3] for i in range(0, len(aufgaben), 3)]:
            print(f"\t\t\t{{ {op_filter(aufgabe[0])} = }} & \\placeholder & {{ {op_filter(aufgabe[1])} = }} & \\placeholder & {{ {op_filter(aufgabe[2])} = }} & \\placeholder \\\\", file=ausgabe)
        print("\t\t\\end{tblr}\n\t\\centering Benötigte Zeit:\\strut~\\placeholderx{7em} \n\t\\end{mdframed}", file=ausgabe)

def main() -> int:
    """\
        Very simply the main entry point to this script
    """
    random.seed()

    schreib_aufgaben("aufgaben-plus-1op-bis-20.tex", aufgaben_mix(30, (1, 20), None, 1, "+"))
    schreib_aufgaben("aufgaben-minus-1op-bis-20.tex", aufgaben_mix(30, (1, 20), None, 1, "-"))
    schreib_aufgaben("aufgaben-plusminus-1op-bis-20.tex", aufgaben_mix(30, (1, 20), None, 1, "+-"))
    schreib_aufgaben("aufgaben-plusminus-1op-bis-20-zwo.tex", aufgaben_mix(30, (1, 20), None, 1, "+-"))

    schreib_aufgaben("aufgaben-plus-1op-bis-100.tex", aufgaben_mix(30, (1, 100), None, 1, "+"))
    schreib_aufgaben("aufgaben-minus-1op-bis-100.tex", aufgaben_mix(30, (1, 100), None, 1, "-"))
    schreib_aufgaben("aufgaben-plusminus-1op-bis-100.tex", aufgaben_mix(30, (1, 100), None, 1, "+-"))
    schreib_aufgaben("aufgaben-plusminus-1op-bis-100-zwo.tex", aufgaben_mix(30, (1, 100), None, 1, "+-"))

    schreib_aufgaben("aufgaben-plus-2op-bis-100.tex", aufgaben_mix(30, (1, 100), None, 2, "+"))
    schreib_aufgaben("aufgaben-minus-2op-bis-100.tex", aufgaben_mix(30, (1, 100), None, 2, "-"))
    schreib_aufgaben("aufgaben-plusminus-2op-bis-100.tex", aufgaben_mix(30, (1, 100), None, 2, "+-"))
    schreib_aufgaben("aufgaben-plusminus-2op-bis-100-zwo.tex", aufgaben_mix(30, (1, 100), None, 2, "+-"))

    schreib_aufgaben("aufgaben-multiplikation-1op-bis-15x15.tex", aufgaben_mix(30, (1, 15*15), None, 1, "*"))
    schreib_aufgaben("aufgaben-division-1op-bis-15x15.tex", aufgaben_mix(30, (1, 15*15), None, 1, "/"))
    schreib_aufgaben("aufgaben-multidivi-1op-bis-15x15.tex", aufgaben_mix(30, (1, 15*15), None, 1, "*/"))
    schreib_aufgaben("aufgaben-multidivi-1op-bis-15x15-zwo.tex", aufgaben_mix(30, (1, 15*15), None, 1, "*/"))

    schreib_aufgaben("aufgaben-multiplikation-1op-bis-10x10.tex", aufgaben_mix(30, (1, 10*10), None, 1, "*"))
    schreib_aufgaben("aufgaben-division-1op-bis-10x10.tex", aufgaben_mix(30, (1, 10*10), None, 1, "/"))
    schreib_aufgaben("aufgaben-multidivi-1op-bis-10x10.tex", aufgaben_mix(30, (1, 10*10), None, 1, "*/"))
    schreib_aufgaben("aufgaben-multidivi-1op-bis-10x10-zwo.tex", aufgaben_mix(30, (1, 10*10), None, 1, "*/"))
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
