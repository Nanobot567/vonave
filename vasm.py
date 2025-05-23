#! /bin/python3

# vonave assembler

import helpers

import binascii
import re

import argparse

def strToPaddedHex(st, pad=8):
    return helpers.padhexa(hex(int(st)), pad)

def strToHexStr(st):
    endhex = ""

    for i in st:
        endhex += str(hex(ord(i)))[2:]

    return endhex

def addToByteIndex(str):
    return int(len(str) / 2)


class VonaveAssemblerException(Exception):
    pass


def assemble(asm):
    graphicsMode = "00"
    version = "00"
    displaywidth = "0040"
    displayheight = "0040"
    bits = "10" # 16 TODO: make this so it's actually accurate (bc for some reason 4-bit 4color.vva works..)

    labels = {}
    defs = {}
    datas = {}
    interrupts = {
        "kb": 0,
        "mouse": 0,
        "click": 0
    }

    header = [strToHexStr("VVX")]
    byt = []

    byteIndex = helpers.HEADER_LENGTH # header is always 9 bytes long

    for x in re.finditer(r"^\.include\s+(\S+)", asm, flags=re.MULTILINE): # include file with .include
        try:
            includefile = open(x.group().split(" ")[1].strip("\""))
        
            asm = asm.replace(x.group(), includefile.read())

            includefile.close()
        except FileNotFoundError:
            raise VonaveAssemblerException(f"include file not found: {x.group()}")

    for x in re.finditer(r"\".+\"", asm): # replace anything with quotes with hex representation
        txt = x.group().strip("\"")

        hexes = []

        for i in txt:
            hexes.append(hex(ord(i))[2:])

        hexes = "".join(hexes).replace("\\n", "10")

        asm = asm.replace(x.group(), hexes)
        
    asm = re.sub(r"(?<!\\)\'.", lambda x: str(ord(x.group(0)[1])), asm)

    for line in asm.split("\n"):
        line = line.split(";")[0].lstrip()

        if line.startswith(".version"):
            version = strToPaddedHex(line.split(" ")[1], 2)

        elif line.startswith(".width"):
            displaywidth = strToPaddedHex(line.split(" ")[1], 4)

        elif line.startswith(".height"):
            displayheight = strToPaddedHex(line.split(" ")[1], 4)

        elif line.startswith(".graphics"):
            graphicsMode = strToPaddedHex(line.split(" ")[1], 2)

        elif line.startswith(".bits"):
            bits = strToPaddedHex(line.split(" ")[1], 2)

        elif line.startswith(".data"):
            datas[line.split(" ")[1]] = line.split(" ")[2]

        elif line.startswith("interrupt"):
            interrupts[line.split(" ")[1]] = byteIndex
            
        elif line.startswith("label"):
            name = line.split(" ")[1]
            labels[name] = byteIndex - helpers.HEADER_LENGTH
        else:
            for k in helpers.INSTRUCTIONS.keys():
                if k == line.split(" ")[0]:
                    inst = helpers.INSTRUCTIONS[k]

                    byteIndex += helpers.INSTRUCTION_HEADER_LENGTH + 1 + (len(inst.arguments) * int(int(bits, 16) / 4))

    totalByteLen = byteIndex

    datasHex = {}
    datasAddrs = {}

    tmpLen = totalByteLen

    for k, v in datas.items():
        datasHex[k] = v
        datasAddrs[k] = tmpLen - helpers.HEADER_LENGTH
        tmpLen += int(len(v) / 2)

    byteIndex = helpers.HEADER_LENGTH

    for line in asm.split("\n"):
        oldBytLen = 0

        for b in byt:
            oldBytLen += int((len(b) + 1) / 2)

        if line.startswith(";"):
            continue

        line = line.split(";")[0].lstrip()

        if line.startswith("def"):
            name = line.split(" ")[1]
            defs[name] = line.split(" ")[2]

        for k in helpers.INSTRUCTIONS.keys():
            if k == line.split(" ")[0]:
                inst = helpers.INSTRUCTIONS[k]
                cur = [inst.hexOpcode]

                for k in defs.keys():
                    line = line.replace(k, defs[k])

                spl = re.split(" |,", line)

                for i in range(len(spl) - 1, 0, -1):
                    if not spl[i]:
                        spl.pop(i)

                if len(spl) < len(inst.arguments) + 1 or len(spl) > len(inst.arguments) + 1:
                    raise VonaveAssemblerException(f"'{inst.name}' takes {len(inst.arguments)} arg(s), not {len(spl) - 1}.")

                for i in range(1, len(inst.arguments)):
                    stripped = spl[i].lstrip("#").lstrip("$")

                    if stripped in helpers.READ_ONLY_REGISTERS:
                        raise VonaveAssemblerException(f"\"{inst.name}\"'s argument {i} does not allow read only registers ('{stripped}' is read only)")


                argprops = [
                    {
                        "immediates": True,
                        "registers": False,
                        "fromROM": False
                    },
                    {
                        "immediates": True,
                        "registers": False,
                        "fromROM": False
                    }
                ]

                try:
                    for i in range(len(inst.arguments)):
                        if spl[i + 1].startswith("#"): # addresses are accessed through # now
                            argprops[i]["immediates"] = False

                        stripped = spl[i + 1].lstrip("#")

                        if stripped.startswith("$"):
                            argprops[i]["fromROM"] = True
     
                        stripped = stripped.lstrip("$")

                        if stripped in labels.keys():
                            spl[i + 1] = str(labels[stripped])
                        elif stripped in datas.keys():
                            spl[i + 1] = str(datasAddrs[stripped])
                        elif stripped.isalpha():
                            if stripped in helpers.REGISTERS:
                                argprops[i]["registers"] = True
                                spl[i + 1] = hex(helpers.REGISTERS.index(stripped))
                            elif len(stripped) == 1:
                                raise VonaveAssemblerException(f"{stripped} is not a valid register")
                except IndexError:
                    pass

                for k in argprops[0].keys():
                    appn = "00"

                    if argprops[0][k] and argprops[1][k]:
                        appn = "03"
                    elif argprops[1][k]:
                        appn = "02"
                    elif argprops[0][k]:
                        appn = "01"
                        
                    cur.append(appn)

                try:
                    cur.append(helpers.padhexa(spl[1].strip("#").strip("$"), int(int(bits, 16) / 2)))
                    cur.append(helpers.padhexa(spl[2].strip("#").strip("$"), int(int(bits, 16) / 2)))
                except IndexError:
                    pass

                byt.append("".join(cur))

                break

        newBytLen = 0

        for b in byt:
            newBytLen += int((len(b) + 1) / 2)

        byteIndex += newBytLen - oldBytLen

    header.append(version)
    header.append(displaywidth)
    header.append(displayheight)
    header.append(graphicsMode)
    header.append(bits)

    for k, v in datas.items():
        byt.append(datasHex[k])

    for k in helpers.INTERRUPTS:
        header.append(helpers.padhexa(str(interrupts[k]), int(int(bits, 16) / 4)))

    return "".join(header) + "".join(byt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="vasm", description="vonave assembler")
    parser.add_argument("input", help="input file path", type=str)
    parser.add_argument("-o", "--output", help="output file path")
    args = parser.parse_args()

    infile = args.input

    try:
        with open(infile, "r") as i:

            outfile = args.output

            if not args.output:
                outfile = ".".join(infile.split(".")[:-1]) + ".vvx"

            with open(outfile, "wb") as f:
                out = assemble(i.read())
                print(out)

                f.write(binascii.unhexlify(out))
    except FileNotFoundError:
        parser.error(f"file {infile} not found.")
