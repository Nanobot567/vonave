def padhexa(x, len=8):
    if not x.startswith("0x"): # just a regular int
        x = hex(int(x))

    return x[2:].zfill(len)

class Argument:
    ANY = 1
    WRITABLE = 2

class Instruction:
    opcode = -1

    def __init__(self, name="nop", arguments=[]):
        Instruction.opcode += 1

        self.name = name
        self.opcode = Instruction.opcode
        self.hexOpcode = padhexa(hex(self.opcode), 2)
        self.arguments = arguments

INSTRUCTIONS = {
    "nop": Instruction("nop"),
    "mov": Instruction("mov", [Argument.WRITABLE, Argument.ANY]),
    "swp": Instruction("swp", [Argument.WRITABLE, Argument.WRITABLE]),
    "inc": Instruction("inc", [Argument.WRITABLE]),
    "dec": Instruction("dec", [Argument.WRITABLE]),
    "add": Instruction("add", [Argument.WRITABLE, Argument.ANY]),
    "sub": Instruction("sub", [Argument.WRITABLE, Argument.ANY]),
    "mul": Instruction("mul", [Argument.WRITABLE, Argument.ANY]),
    "div": Instruction("div", [Argument.WRITABLE, Argument.ANY]),
    "cmp": Instruction("cmp", [Argument.ANY, Argument.ANY]),
    "jmp": Instruction("jmp", [Argument.ANY]),
    "jeq": Instruction("jeq", [Argument.ANY]),
    "jne": Instruction("jne", [Argument.ANY]),
    "jmt": Instruction("jmt", [Argument.ANY]),
    "jme": Instruction("jme", [Argument.ANY]),
    "jlt": Instruction("jlt", [Argument.ANY]),
    "jle": Instruction("jle", [Argument.ANY]),
    "call": Instruction("call", [Argument.ANY]),
    "cleq": Instruction("cleq", [Argument.ANY]),
    "clne": Instruction("clne", [Argument.ANY]),
    "clmt": Instruction("clmt", [Argument.ANY]),
    "clme": Instruction("clme", [Argument.ANY]),
    "cllt": Instruction("cllt", [Argument.ANY]),
    "clle": Instruction("clle", [Argument.ANY]),
    "ret": Instruction("ret"),
    "push": Instruction("push", [Argument.ANY]),
    "pop": Instruction("pop", [Argument.WRITABLE]),
    "and": Instruction("and", [Argument.WRITABLE, Argument.ANY]),
    "or": Instruction("or", [Argument.WRITABLE, Argument.ANY]),
    "xor": Instruction("xor", [Argument.WRITABLE, Argument.ANY]),
    "not": Instruction("not", [Argument.WRITABLE]),
    "shr": Instruction("shr", [Argument.WRITABLE]),
    "shl": Instruction("shl", [Argument.WRITABLE]),
    "wipe": Instruction("wipe"),
    "palette": Instruction("palette", [Argument.ANY, Argument.ANY]),
    "color": Instruction("color", [Argument.ANY]),
    "pxl": Instruction("pxl", [Argument.ANY, Argument.ANY]),
    "gpxl": Instruction("gpxl", [Argument.WRITABLE, Argument.WRITABLE]),
    "pxe": Instruction("pxe", [Argument.ANY]),
    "pxi": Instruction("pxi"),
    "pxd": Instruction("pxd"),
    "pxa": Instruction("pxa", [Argument.ANY]),
    "pxs": Instruction("pxs", [Argument.ANY]),
    "pye": Instruction("pye", [Argument.ANY]),
    "pyi": Instruction("pxi"),
    "pyd": Instruction("pyd"),
    "pya": Instruction("pya", [Argument.ANY]),
    "pys": Instruction("pys", [Argument.ANY]),
    "point": Instruction("point"),
    "line": Instruction("line", [Argument.ANY, Argument.ANY]),
    "rect": Instruction("rect", [Argument.ANY, Argument.ANY]),
    "frect": Instruction("frect", [Argument.ANY, Argument.ANY]),
    "char": Instruction("char", [Argument.ANY]),
    "charw": Instruction("charw", [Argument.ANY]),
    "mouse": Instruction("mouse", [Argument.WRITABLE, Argument.WRITABLE]),
    "click": Instruction("click", [Argument.WRITABLE]),
    "kb": Instruction("kb", [Argument.WRITABLE]),
    "beep": Instruction("beep", [Argument.ANY]),
    "wait": Instruction("wait", [Argument.ANY]),
    "rnd": Instruction("rnd", [Argument.WRITABLE, Argument.ANY]),
    "log": Instruction("log", [Argument.ANY]),
    "halt": Instruction("halt"),
}

REGISTERS = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p"
]

READ_ONLY_REGISTERS = [
    "a",
    "c",
    "e"
]

HEADER_LENGTH = 10
INSTRUCTION_HEADER_LENGTH = 2

PALETTE_ONEBIT = [(0, 0, 0), (255, 255, 255)]
PALETTE_TWOBIT = [(0, 0, 0), (255, 90, 0), (110, 0, 255), (255, 255, 255)]
PALETTE_FOURBIT = [(0, 0, 0),
                   (0, 0, 170),
                   (0, 170, 0),
                   (0, 170, 170),
                   (170, 0, 0),
                   (170, 0, 170),
                   (170, 85, 0),
                   (170, 170, 170),
                   (85, 85, 85),
                   (85, 85, 255),
                   (85, 255, 85),
                   (85, 255, 255),
                   (255, 85, 85),
                   (255, 85, 255),
                   (255, 255, 85),
                   (255, 255, 255)]
PALETTE_EIGHTBIT = []
PALETTE_SIXTEENBIT = []
