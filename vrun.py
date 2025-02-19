#! /bin/python3

import argparse
import binascii

from vasm import assemble
from vemu import emulate

parser = argparse.ArgumentParser(prog="vrun", description="vonave assembler + emulator (does not build .vvx)")
parser.add_argument("input", help="input .vva path", type=str)
args = parser.parse_args()

infile = args.input

try:
    with open(infile, "r") as i:
        emulate(binascii.unhexlify(assemble(i.read())))
except FileNotFoundError:
    parser.error(f"file {infile} not found.")
