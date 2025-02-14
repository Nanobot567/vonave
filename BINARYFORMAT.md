# binary format docs

`vonave`'s binary format (.vvx).

| offset    | description                |
| --------- | -------------------------- |
| `00`-`02` | vonave magic (`VVX`)       |
| `03`      | format version number      |
| `04`-`05` | display width (in pixels)  |
| `06`-`07` | display height (in pixels) |
| `08`      | graphics mode              |
| `09`      | bit width                  |

for each instruction, there is...

- a 4-bit opcode `00`-`FF`
- the opcode immediate mode
	- `00`: no immediates
	- `01`: argument 1 is immediate
	- `02`: argument 2 is immediate
	- `03`: both arguments are immediate
- register?
	- `00`: no arguments are registers
	- `01`: arg 1 is a register
	- `02`: arg 2 is a register
	- `03`: both args are registers
- convert to char value?
	- `00`: none
	- `01`: A
	- `02`: B
	- `03`: both