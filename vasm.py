# assemble

import helpers

import binascii
import re

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
    graphicsMode = "0"
    version = "0"
    displaywidth = "64"
    displayheight = "64"
    bits = "16"

    labels = {}

    header = [strToHexStr("VVX")]
    byt = []

    byteIndex = helpers.HEADER_LENGTH # header is always 9 bytes long

    for x in re.finditer(r"\.include\s+(\S+)", asm): # include stuff
        try:
            includefile = open(x.group().split(" ")[1].strip("\""))
        
            asm = asm.replace(x.group(), includefile.read())

            includefile.close()
        except FileNotFoundError:
            raise VonaveAssemblerException(f"include file not found: {x.group()}")

    for line in asm.split("\n"):
        oldBytLen = 0

        for b in byt:
            oldBytLen += int((len(b) + 1) / 2)

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

        elif line.startswith("label"): # TODO: support labels not seen yet
            name = line.split(" ")[1]
            labels[name] = byteIndex - helpers.HEADER_LENGTH

        for k in helpers.INSTRUCTIONS.keys():
            if k == line.split(" ")[0]:
                inst = helpers.INSTRUCTIONS[k]
                cur = [inst.hexOpcode]

                spl = re.split(" |,", line)

                for i in range(len(spl) - 1, 0, -1):
                    if not spl[i]:
                        spl.pop(i)

                if len(spl) < len(inst.arguments) + 1 or len(spl) > len(inst.arguments) + 1:
                    raise VonaveAssemblerException(f"'{inst.name}' takes {len(inst.arguments)} arg(s), not {len(spl) - 1}.")

                for i in range(1, len(inst.arguments)):
                    stripped = spl[i].lstrip("#")

                    if stripped in helpers.READ_ONLY_REGISTERS:
                        raise VonaveAssemblerException(f"\"{inst.name}\"'s argument {i} does not allow read only registers ('{stripped}' is read only)")

                arg1i, arg2i = False, False
                arg1r, arg2r = False, False

                try: # NOTE: maybe compress this down a lil
                    if spl[1].startswith("#"):
                        arg1i = True

                    stripped = spl[1].lstrip("#")

                    if stripped in labels.keys():
                        spl[1] = str(labels[stripped])
                    elif stripped.isalpha():
                        if stripped in helpers.REGISTERS:
                            arg1r = True
                            spl[1] = hex(helpers.REGISTERS.index(stripped))
                        elif len(stripped) == 1:
                            raise VonaveAssemblerException(f"{stripped} is not a valid register")

                    if spl[2].startswith("#"):
                        arg2i = True

                    stripped = spl[2].lstrip("#")

                    if stripped.isalpha():
                        if stripped in helpers.REGISTERS:
                            arg2r = True
                            spl[2] = hex(helpers.REGISTERS.index(stripped))
                        else:
                            raise VonaveAssemblerException(f"{stripped} is not a valid register")
                except IndexError:
                    pass

                appn = "00"

                if arg1i and arg2i:
                    appn = "03"
                elif arg2i:
                    appn = "02"
                elif arg1i:
                    appn = "01"

                cur.append(appn)

                appn = "00"

                if arg1r and arg2r:
                    appn = "03"
                elif arg2r:
                    appn = "02"
                elif arg1r:
                    appn = "01"

                cur.append(appn)

                try:
                    cur.append(helpers.padhexa(spl[1].strip("#"), int(int(bits, 16) / 2)))
                    cur.append(helpers.padhexa(spl[2].strip("#"), int(int(bits, 16) / 2)))
                except IndexError:
                    pass

                byt.append("".join(cur))

        newBytLen = 0

        for b in byt:
            newBytLen += int((len(b) + 1) / 2)

        byteIndex += newBytLen - oldBytLen

    header.append(version)
    header.append(displaywidth)
    header.append(displayheight)
    header.append(graphicsMode)
    header.append(bits)

    return "".join(header) + "".join(byt)

with open("asm.vva", "r") as i:
    with open("asm.vvx", "wb") as f:
        out = assemble(i.read())
        print(out)

        f.write(binascii.unhexlify(out))
