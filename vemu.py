#! /bin/python3

# vonave emulator

import binascii
from sys import stdout
import pygame
import random
import argparse

from helpers import HEADER_LENGTH, INSTRUCTION_HEADER_LENGTH, INSTRUCTIONS, PALETTE_FOURBIT, PALETTE_ONEBIT, PALETTE_TWOBIT, Argument, padhexa

SCALE = 7

INSTRUCTION_KEYS = []

for k in INSTRUCTIONS.keys():
    INSTRUCTION_KEYS.append(k)

class VonaveEmulatorException(Exception):
    pass


def emulate(data):

    ram = [0] * (2^16)
    registers = [0] * 16

    def parseBlock(data, ptr):
        global INSTRUCTION_KEYS

        try:
            byte = data[ptr]
        except IndexError:
            return None, None, None, ptr

        try:
            inst = INSTRUCTIONS[INSTRUCTION_KEYS[int(byte)]]
        except IndexError:
            raise VonaveEmulatorException(f"invalid instruction {byte} at {hex(ptr)}")

        args = []

        immediates = 0
        registers = 0

        try:
            immediates = data[ptr+1]
            registers = data[ptr+2] 
        except IndexError:
            pass
        # convertToChar = data[ptr+3]

        ptr += INSTRUCTION_HEADER_LENGTH + 1

        try:
            if inst.arguments[0]:
                byts = data[ptr:ptr+int(bits / 4)]

                dat = byts

                if immediates == 0 or immediates == 2:
                    hx = hex(ram[int.from_bytes(byts)])

                    if len(hx[2:]) % 2 == 1:
                        hx = padhexa(hx, len(hx) + 1)

                    dat = binascii.unhexlify(hx[2:])

                args.append(dat)

                ptr += int(bits / 4)
            
            if inst.arguments[1]:
                byts = data[ptr:ptr+int(bits / 4)]

                dat = byts

                if immediates == 0 or immediates == 1:
                    hx = hex(ram[int.from_bytes(byts)]).lstrip("0x")

                    if len(hx) % 2 == 1:
                        hx = padhexa("0x" + hx, len(hx) + 1)

                    dat = binascii.unhexlify(hx)

                args.append(dat)

                ptr += int(bits / 4)

        except IndexError:
            pass

        return inst, args, registers, ptr

    asmver = data[4]
    displaywidth = int.from_bytes(data[5:6])
    displayheight = int.from_bytes(data[7:8])
    gfxmode = data[8]
    bits = data[9]

    palette = []

    screen = None
    win = pygame.Surface((0, 0))

    if gfxmode > 0:
        pygame.init()
        pygame.display.set_caption("vonave")
        pygame.display.set_icon(pygame.surface.Surface((0, 0)))
        pygame.freetype.init()

        defaultfont = pygame.freetype.Font("pzim3x5.ttf", 10)

        screen = pygame.display.set_mode((displaywidth * SCALE, displayheight * SCALE))
        win = pygame.Surface((displaywidth, displayheight))

        if gfxmode == 1:
            palette = PALETTE_ONEBIT.copy()
        elif gfxmode == 2:
            palette = PALETTE_TWOBIT.copy()
        elif gfxmode == 3:
            palette = PALETTE_FOURBIT.copy()

        color = palette[-1]
        colorindex = len(palette) - 1

    running = True

    ptr = HEADER_LENGTH

    pixelpos = [0, 0]
    cmp = [0, 0]
    stack = []
    callstack = []
 
    keydown = 0

    while running:
        if gfxmode > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    keydown = event.key

        instruction, args, rgrs, ptr = parseBlock(data, ptr)

        if instruction:
            iname = instruction.name

            intarg0, intarg1 = 0, 0

            try:
                intarg0 = int.from_bytes(args[0])
                intarg1 = int.from_bytes(args[1])
            except IndexError:
                pass

            # print(instruction.name, instruction.opcode, hex(ptr), intarg0, intarg1)

            try:
                match iname:  # TODO: none of these work with registers (writing to registers)
                    case "mov":
                        ram[intarg0] = intarg1
                    case "swp":
                        ram[intarg0], ram[intarg1] = ram[intarg1], ram[intarg0]
                    case "inc":
                        ram[intarg0] += 1
                        # print(ram[intarg0])
                    case "dec":
                        ram[intarg0] -= 1
                    case "add": # TODO: carry byte
                        ram[intarg0] += intarg1
                    case "sub":
                        ram[intarg0] -= intarg1
                    case "cmp":
                        cmp = [intarg0, intarg1]
                    case "jmp": # TODO: possibly compress in some way
                        ptr = intarg0 + HEADER_LENGTH
                    case "jeq":
                        if cmp[0] == cmp[1]:
                            ptr = intarg0 + HEADER_LENGTH
                    case "jne":
                        if cmp[0] != cmp[1]:
                            ptr = intarg0 + HEADER_LENGTH
                    case "jmt":
                        if cmp[0] > cmp[1]:
                            ptr = intarg0 + HEADER_LENGTH
                    case "jme":
                        if cmp[0] >= cmp[1]:
                            ptr = intarg0 + HEADER_LENGTH
                    case "jlt":
                        if cmp[0] < cmp[1]:
                            ptr = intarg0 + HEADER_LENGTH
                    case "jle":
                        if cmp[0] <= cmp[1]:
                            ptr = intarg0 + HEADER_LENGTH
                    case "call":
                        callstack.append(ptr)
                        ptr = intarg0 + HEADER_LENGTH
                    case "cleq":
                        if cmp[0] == cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + HEADER_LENGTH
                    case "clne":
                        if cmp[0] != cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + HEADER_LENGTH
                    case "clmt":
                        if cmp[0] > cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + HEADER_LENGTH
                    case "clme":
                        if cmp[0] >= cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + HEADER_LENGTH
                    case "cllt":
                        if cmp[0] < cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + HEADER_LENGTH
                    case "clle":
                        if cmp[0] <= cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + HEADER_LENGTH
                    case "ret":
                        try:
                            ptr = callstack.pop()
                        except IndexError:
                            pass
                    case "push":
                        stack.append(intarg0)
                    case "pop":
                        ram[intarg0] = stack.pop()
                    case "and":
                        pass
                    case "or":
                        pass
                    case "xor":
                        pass
                    case "not":
                        pass
                    case "shr":
                        pass
                    case "shl":
                        pass
                    case "wipe":
                        win.fill(palette[0], (0, 0, displaywidth, displayheight))
                    case "palette":
                        palette[intarg0] = tuple(args[1])
                        color = palette[colorindex]
                    case "color":
                        color = palette[intarg0]
                        colorindex = intarg0
                    case "pxl":
                        pixelpos = [intarg0, intarg1]
                    case "gpxl":
                        ram[intarg0] = pixelpos[0]
                        ram[intarg1] = pixelpos[1]
                    case "pxe":
                        pixelpos[0] = intarg0
                    case "pxi":
                        pixelpos[0] += 1
                    case "pxd":
                        pixelpos[0] -= 1
                    case "pxa":
                        pixelpos[0] += intarg0
                    case "pxs":
                        pixelpos[0] -= intarg0
                    case "pye":
                        pixelpos[1] = intarg0
                    case "pyi":
                        pixelpos[1] += 1
                    case "pyd":
                        pixelpos[1] -= 1
                    case "pya":
                        pixelpos[1] += intarg0
                    case "pys":
                        pixelpos[1] -= intarg0
                    case "point":
                        win.set_at((pixelpos[0], pixelpos[1]), color)
                    case "line":
                        pygame.draw.line(win, color, (pixelpos[0], pixelpos[1]), (intarg0, intarg1))
                    case "rect":
                        pygame.draw.rect(win, color, (pixelpos[0], pixelpos[1], intarg0, intarg1), width=1)
                    case "frect":
                        pygame.draw.rect(win, color, (pixelpos[0], pixelpos[1], intarg0, intarg1))
                    case "char":
                        # pass
                        text_surface, rect = defaultfont.render(chr(intarg0), color)
                        win.blit(text_surface, (pixelpos[0], pixelpos[1]))
                    case "charw":
                        text_surface, rect = defaultfont.render(chr(intarg0), color)
                        win.blit(text_surface, (pixelpos[0], pixelpos[1]))

                        if chr(intarg0) == " ":
                            pixelpos[0] += 2
                        else:
                            pixelpos[0] += text_surface.get_width() + 1
                    case "mouse":
                        pass
                    case "click":
                        pass
                    case "kb":
                        ram[intarg0] = keydown
                    case "beep":
                        pass
                    case "wait":
                        pygame.time.delay(intarg0)
                    case "rnd":
                        ram[intarg0] = random.randint(0, intarg1)
                    case "log":
                        try:
                            stdout.write(args[0].decode())
                            stdout.flush()
                        except UnicodeDecodeError:
                            pass
                    case "halt":
                        print("\n[VNV] CPU halted.")
                        running = False
            except UnboundLocalError:
                pass
            except AttributeError:
                pass
        # ptr += 1

        if gfxmode > 0:
            scaledwin = pygame.transform.scale(win, screen.get_size())
            screen.blit(scaledwin, (0, 0))
            pygame.display.flip()

    if gfxmode > 0:
        pygame.quit()

    return 0

parser = argparse.ArgumentParser(prog="vemu", description="vonave CPU emulator")
parser.add_argument("vvx", help="vonave executable (.vvx)", type=str)
args = parser.parse_args()

try:
    with open(args.vvx, "rb") as f:
        data = f.read()
except FileNotFoundError:
    parser.error(f"file {args.vvx} not found.")

emulate(data)
