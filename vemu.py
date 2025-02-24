#! /bin/python3

# vonave emulator

import binascii
from sys import intern, stdout
import pygame
import random
import argparse

from helpers import BIT_DEPENDENT_ARGS_COUNT, HEADER_LENGTH, INSTRUCTION_HEADER_LENGTH, INSTRUCTIONS, INTERRUPTS, PALETTE_FOURBIT, PALETTE_ONEBIT, PALETTE_TWOBIT, Argument, padhexa

SCALE = 8

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
            return None, None, None, None, ptr

        try:
            inst = INSTRUCTIONS[INSTRUCTION_KEYS[int(byte)]] # NOTE: fails if at end of program as well
        except IndexError:
            raise VonaveEmulatorException(f"invalid instruction {byte} at {hex(ptr)}")

        args = []

        immediates = 0
        registers = 0
        dataAtAddress = 0

        try:
            immediates = data[ptr+1]
            registers = data[ptr+2] 
            dataAtAddress = data[ptr+3]
        except IndexError:
            pass

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

        return inst, args, registers, dataAtAddress, ptr

    asmver = data[4]
    displaywidth = int.from_bytes(data[4:6])
    displayheight = int.from_bytes(data[6:8])
    gfxmode = data[8]
    bits = data[9]
    
    interrupts = {}

    for i in range(BIT_DEPENDENT_ARGS_COUNT):
        ptr = (i * (int(bits / 8))) + HEADER_LENGTH

        interrupts[INTERRUPTS[i]] = data[ptr:ptr+(int(bits / 8))]

        if interrupts[INTERRUPTS[i]] == b"\x00\x00":
            interrupts[INTERRUPTS[i]] = None

    palette = []

    screen = None
    win = pygame.Surface((0, 0))

    if gfxmode > 0:
        pygame.init()
        pygame.display.set_caption("vonave")
        pygame.display.set_icon(pygame.surface.Surface((0, 0)))
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])
        pygame.freetype.init()

        defaultfont = pygame.freetype.Font("default.ttf", 5)

        screen = pygame.display.set_mode((displaywidth * SCALE, displayheight * SCALE), pygame.DOUBLEBUF)
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

    ACTUAL_HEADER_LENGTH = HEADER_LENGTH + (BIT_DEPENDENT_ARGS_COUNT * int(bits / 8))

    ptr = ACTUAL_HEADER_LENGTH

    pixelpos = [0, 0]
    cmp = [0, 0]
    stacks = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []] # TODO: create Stack class which prevents writing more than (num) values
    currentStack = 0
    callstack = []

    interruptStack = []
 
    keydown = 0
    mousepos = [0, 0]
    mousebuttons = [False, False, False]

    while running:
        if gfxmode > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    keydown = event.key

                    if interrupts["kb"]:
                        interruptStack.append("kb")
                        callstack.append(ptr)
                        ptr = int.from_bytes(interrupts["kb"]) + 2

                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    mb = pygame.mouse.get_pressed()
                    mousebuttons = [0, 0, 0]

                    for i, v in enumerate(mb):
                        if v:
                            mousebuttons[i] = 1

                    if interrupts["click"]:
                        interruptStack.append("click")
                        callstack.append(ptr)
                        ptr = int.from_bytes(interrupts["click"]) + 6

                elif event.type == pygame.MOUSEMOTION:
                    mp = pygame.mouse.get_pos()
                    mousepos[0] = int(mp[0] / SCALE)
                    mousepos[1] = int(mp[1] / SCALE)

                    if interrupts["mouse"]:
                        interruptStack.append("mouse")
                        callstack.append(ptr)
                        ptr = int.from_bytes(interrupts["mouse"]) + 6 # don't know why these arbitrary numbers work but-

        instruction, args, rgrs, fromROM, ptr = parseBlock(data, ptr)

        if instruction:
            drew = False

            iname = instruction.name

            intarg0, intarg1 = 0, 0

            try:
                arg0 = args[0]

                if fromROM == 1 or fromROM == 3: # NOTE: possibly load everything into RAM, so there's no fromROM at all???
                    arg0 = padhexa(hex(data[ram[int.from_bytes(arg0)] + HEADER_LENGTH]), int(bits / 2))
                    arg0 = binascii.unhexlify(arg0)

                intarg0 = int.from_bytes(arg0)

                arg1 = args[1]

                if fromROM == 2 or fromROM == 3:
                    arg1 = ram[int.from_bytes(arg1)]

                intarg1 = int.from_bytes(arg1)
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
                        ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "jeq":
                        if cmp[0] == cmp[1]:
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "jne":
                        if cmp[0] != cmp[1]:
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "jmt":
                        if cmp[0] > cmp[1]:
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "jme":
                        if cmp[0] >= cmp[1]:
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "jlt":
                        if cmp[0] < cmp[1]:
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "jle":
                        if cmp[0] <= cmp[1]:
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "call":
                        callstack.append(ptr)
                        ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "cleq":
                        if cmp[0] == cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "clne":
                        if cmp[0] != cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "clmt":
                        if cmp[0] > cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "clme":
                        if cmp[0] >= cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "cllt":
                        if cmp[0] < cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "clle":
                        if cmp[0] <= cmp[1]:
                            callstack.append(ptr)
                            ptr = intarg0 + ACTUAL_HEADER_LENGTH
                    case "ret":
                        try:
                            ptr = callstack.pop()
                            interruptStack.pop()
                        except IndexError:
                            pass
                    case "push":
                        stacks[currentStack].append(intarg0)
                    case "pop":
                        ram[intarg0] = stacks[currentStack].pop()
                    case "popa":
                        stacks[currentStack] = []
                    case "stack":
                        currentStack = intarg0
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
                        drew = True
                    case "palette":
                        palette[intarg0] = tuple(arg1)
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
                        drew = True
                    case "line":
                        pygame.draw.line(win, color, (pixelpos[0], pixelpos[1]), (intarg0, intarg1))
                        drew = True
                    case "rect":
                        pygame.draw.rect(win, color, (pixelpos[0], pixelpos[1], intarg0, intarg1), width=1)
                        drew = True
                    case "frect":
                        pygame.draw.rect(win, color, (pixelpos[0], pixelpos[1], intarg0, intarg1))
                        drew = True
                    case "char":
                        try:
                            text_surface, rect = defaultfont.render(chr(intarg0), color)
                            win.blit(text_surface, (pixelpos[0], pixelpos[1]))
                        except ValueError:
                            pass
                        drew = True
                    case "charw":
                        try:
                            text_surface, rect = defaultfont.render(chr(intarg0), color)
                            win.blit(text_surface, (pixelpos[0], pixelpos[1]))

                            if chr(intarg0) == " ":
                                pixelpos[0] += 2
                            else:
                                pixelpos[0] += text_surface.get_width() + 1
                        except ValueError:
                            pass
                        drew = True
                    case "glyphw":
                        metrics = defaultfont.get_metrics(chr(intarg0))

                        if metrics[0]:
                            horiz_advance_width = metrics[0][4]
                            if chr(intarg0) == " ":
                                horiz_advance_width -= 1
                            ram[intarg1] = int(horiz_advance_width)
                        else:
                            ram[intarg1] = 0
                    case "glyphh": # possibly change name, as glyph isn't even taken into account lol
                        fh = defaultfont.height

                        ram[intarg1] = fh
                    case "idata":
                        try:
                            if interruptStack[-1] == "kb":
                                if intarg1 == 0:
                                    ram[intarg0] = keydown
                            elif interruptStack[-1] == "mouse":
                                if intarg1 == 0:
                                    ram[intarg0] = mousepos[0]
                                elif intarg1 == 1:
                                    ram[intarg0] = mousepos[1]
                            elif interruptStack[-1] == "click":
                                if intarg1 == 0:
                                    ram[intarg0] = mousebuttons[0] # left
                                elif intarg1 == 1:
                                    ram[intarg0] = mousebuttons[2] # right
                                elif intarg1 == 2:
                                    ram[intarg0] = mousebuttons[1] # middle
                        except IndexError:
                            pass
                    case "mouse":
                        ram[intarg0] = mousepos[0]
                        ram[intarg1] = mousepos[1]
                    case "click":
                        cl = mousebuttons

                        ram[intarg0] = 0

                        if cl[0]:
                            ram[intarg0] = 1
                        elif cl[1]:
                            ram[intarg0] = 2
                    case "kb":
                        ram[intarg0] = keydown
                    case "rkb":
                        keydown = 0
                    case "beep":
                        pass
                    case "wait":
                        pygame.time.delay(intarg0)
                    case "rnd":
                        ram[intarg0] = random.randint(0, intarg1)
                    case "log":
                        try:
                            stdout.write(arg0.decode())
                            stdout.flush()
                        except UnicodeDecodeError:
                            pass
                    case "halt":
                        print("\n[VNV] CPU halted.")
                        running = False

                if pixelpos[0] > displaywidth:
                    pixelpos[0] = pixelpos[0] - displaywidth
                elif pixelpos[0] < 0:
                    pixelpos[0] = displaywidth - abs(pixelpos[0])

                if pixelpos[1] > displaywidth:
                    pixelpos[1] = pixelpos[1] - displaywidth
                elif pixelpos[1] < 0:
                    pixelpos[1] = displaywidth - abs(pixelpos[1])

            except UnboundLocalError:
                pass
            except AttributeError:
                pass
        # ptr += 1

        if gfxmode > 0:
            scaledwin = pygame.transform.scale(win, screen.get_size())
            screen.blit(scaledwin, (0, 0))
            if drew:
                pygame.display.flip()

    if gfxmode > 0:
        pygame.quit()

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="vemu", description="vonave CPU emulator")
    parser.add_argument("vvx", help="vonave executable (.vvx)", type=str)
    args = parser.parse_args()

    try:
        with open(args.vvx, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        parser.error(f"file {args.vvx} not found.")

    emulate(data)
