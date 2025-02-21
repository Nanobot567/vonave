# CPU docs

## instructions

- (register) = register `a`-`p` (`00`-`0F`)
- non-immediates (no #) refer to the value in the address specified

## additional notes key
- `WA`: argument A must be writable. if not, results in an error.
- `WB`: argument B must be writable. if not, results in an error.
- `<16`: instruction can only be performed on a less than 16 bit color mode.

| assembler instruction | description                                                                                                                                                    | arguments | additional notes | opcode |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------- | ------ |
| nop                   | no operation                                                                                                                                                   | 0         |                  | 0      |
| mov A,B               | B -> address A                                                                                                                                                 | 2         | WA               | 1      |
| swp A,B               | address B <-> address A                                                                                                                                        | 2         | WA WB            | 2      |
| inc A                 | increment val @ address A by 1                                                                                                                                 | 1         | WA               | 3      |
| dec A                 | decrement val @ address A by 1                                                                                                                                 | 1         | WA               | 4      |
| add A,B               | add B to address A                                                                                                                                             | 2         | WA               | 5      |
| sub A,B               | subtract B from address A                                                                                                                                      | 2         | WA               | 6      |
| mul A,B               | multiply address A by B                                                                                                                                        | 2         | WA               | 7      |
| div A,B               | divide address A by B                                                                                                                                          | 2         | WA               | 8      |
| cmp A,B               | compare B with A                                                                                                                                               | 2         |                  | 9      |
| jmp A                 | jump to address A                                                                                                                                              | 1         |                  | A      |
| jeq A                 | jump if equal to address A                                                                                                                                     | 1         |                  | B      |
| jne A                 | jump if not equal                                                                                                                                              | 1         |                  | C      |
| jmt A                 | jump if more than                                                                                                                                              | 1         |                  | D      |
| jme A                 | jump if more than or equal to                                                                                                                                  | 1         |                  | E      |
| jlt A                 | jump if less than                                                                                                                                              | 1         |                  | F      |
| jle A                 | jump if less than or equal to                                                                                                                                  | 1         |                  | 10     |
| call A                | call function at address A                                                                                                                                     | 1         |                  | 11     |
| cleq A                | call if equal to address A                                                                                                                                     | 1         |                  | 12     |
| clne A                | call if not equal                                                                                                                                              | 1         |                  | 13     |
| clmt A                | call if more than                                                                                                                                              | 1         |                  | 14     |
| clme A                | call if more than or equal to                                                                                                                                  | 1         |                  | 15     |
| cllt A                | call if less than                                                                                                                                              | 1         |                  | 16     |
| clle A                | call if less than or equal to                                                                                                                                  | 1         |                  | 17     |
| ret                   | return from subroutine                                                                                                                                         | 0         |                  | 18     |
| push A                | push A to stack                                                                                                                                                | 1         |                  | 19     |
| pop A                 | pop value from stack and place in A                                                                                                                            | 1         | WA               | 1A     |
| popa                  | pop all from stack                                                                                                                                             | 0         |                  | 1B     |
| and A,B               | AND B with A                                                                                                                                                   | 2         | WA               | 1C     |
| or A,B                | OR B with A                                                                                                                                                    | 2         | WA               | 1D     |
| xor A,B               | XOR B with A                                                                                                                                                   | 2         | WA               | 1E     |
| not A                 | NOT A                                                                                                                                                          | 1         | WA               | 1F     |
| shr A                 | shift A right                                                                                                                                                  | 1         | WA               | 20     |
| shl A                 | shift A left                                                                                                                                                   | 1         | WA               | 21     |
| wipe                  | clear screen with palette color 0                                                                                                                              | 0         |                  | 22     |
| palette A,B           | set palette index A to 16-bit color B (with alpha as last byte)                                                                                                | 2         | <16              | 23     |
| color A               | set draw color to palette index A                                                                                                                              | 1         |                  | 24     |
| pxl A,B               | set current pixel position to x A and y B                                                                                                                      | 2         |                  | 25     |
| gpxl A,B              | get current pixel position, and place the x into A and y into B                                                                                                | 2         | WA WB            | 26     |
| pxe A                 | set pixel x to A                                                                                                                                               | 1         |                  | 27     |
| pxi                   | increment pixel x                                                                                                                                              | 0         |                  | 28     |
| pxd                   | decrement pixel x                                                                                                                                              | 0         |                  | 29     |
| pxa A                 | add A to pixel x                                                                                                                                               | 1         |                  | 2A     |
| pxs A                 | subtract A from pixel x                                                                                                                                        | 1         |                  | 2B     |
| pye A                 | set pixel y to A                                                                                                                                               | 1         |                  | 2C     |
| pyi                   | increment pixel y                                                                                                                                              | 0         |                  | 2D     |
| pyd                   | decrement pixel y                                                                                                                                              | 0         |                  | 2E     |
| pya A                 | add A to pixel y                                                                                                                                               | 1         |                  | 2F     |
| pys A                 | subtract A from pixel y                                                                                                                                        | 1         |                  | 30     |
| point                 | set pixel at pixel position to current draw color                                                                                                              | 0         |                  | 31     |
| line A,B              | draw line from current pixel position to x A, y B                                                                                                              | 2         |                  | 32     |
| rect A,B              | draw rect (top left corner at current pixel position) with width A and height B                                                                                | 2         |                  | 33     |
| frect A,B             | fill rect from current pixel position with width A, height B                                                                                                   | 2         |                  | 34     |
| char A                | draw glyph assigned to hex code A at current pixel position                                                                                                    | 1         |                  | 35     |
| charw A               | draw glyph assigned to hex code A at current pixel position, and update pixel position to reflect glyph width (including y position if at the edge of display) | 1         |                  | 36     |
| glyphw A,B            | get glyph A's width and place into address B                                                                                                                   | 2         | WB               | 37     |
| glyphh A,B            | get glyph B's height and place into address B                                                                                                                  | 2         | WB               | 38     |
| mouse A,B             | place mouse x and y positions into addresses A and B                                                                                                           | 2         | WA WB            | 39     |
| click A               | get click status and place into address A                                                                                                                      | 1         | WA               | 3A     |
| kb A                  | place current keyboard keycode into address A                                                                                                                  | 1         | WA               | 3B     |
| rkb                   | reset keyboard keycode                                                                                                                                         | 1         |                  | 3C     |
| beep A                | play square wave at frequency A / 100 kHz                                                                                                                      | 1         |                  | 3D     |
| wait A                | pause execution for A milliseconds                                                                                                                             | 1         |                  | 3E     |
| rnd A,B               | generate random number from 0 to B and place into A                                                                                                            | 2         | WA               | 3F     |
| log A                 | log character A to console                                                                                                                                     | 1         |                  | 40     |
| halt                  | halt execution                                                                                                                                                 | 0         |                  | 41     |
## registers

`vonave` has 16 registers, `a` (internally known as `00`) through p (internally known as `0F`.

- a - conditional register
	- if the last test was true, is maximum value in current bit width (ex. `FFFF` for 16-bit). otherwise, is `0`.
	- read only
- c - carry register
	- contains value left over after mathematical operation
	- read only
- e - error register
	- contains error code if something went wrong :(
	- read only
- b, d, f-p (read / write)

## graphics modes
- `00`: no display (text only)
- `01`: 1-bit mode (each pixel is white or black)
- `02`: 2-bit mode (4 color palette)
- `03`: 4-bit mode (16 color palette)
- `04`: 8-bit mode
- `05`: 16-bit mode

## banks

`vonave` has two banks: one for general RAM, and another for file I/O.

## stacks

`vonave` has 16 stacks, each of which freely readable and writable.