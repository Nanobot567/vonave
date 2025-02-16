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
| and A,B               | AND B with A                                                                                                                                                   | 2         | WA               | 1B     |
| or A,B                | OR B with A                                                                                                                                                    | 2         | WA               | 1C     |
| xor A,B               | XOR B with A                                                                                                                                                   | 2         | WA               | 1D     |
| not A                 | NOT A                                                                                                                                                          | 1         | WA               | 1E     |
| shr A                 | shift A right                                                                                                                                                  | 1         | WA               | 1F     |
| shl A                 | shift A left                                                                                                                                                   | 1         | WA               | 20     |
| wipe                  | clear screen with palette color 0                                                                                                                              | 0         |                  | 21     |
| palette A,B           | set palette index A to 16-bit color B (with alpha as last byte)                                                                                                | 2         | <16              | 22     |
| color A               | set draw color to palette index A                                                                                                                              | 1         |                  | 23     |
| pxl A,B               | set current pixel position to x A and y B                                                                                                                      | 2         |                  | 24     |
| gpxl A,B              | get current pixel position, and place the x into A and y into B                                                                                                | 2         | WA WB            | 25     |
| point                 | set pixel at pixel position to current draw color                                                                                                              | 0         |                  | 26     |
| line A,B              | draw line from current pixel position to x A, y B                                                                                                              | 2         |                  | 27     |
| rect A,B              | draw rect with top left corner at current pixel position to bottom right corner at x A, y B                                                                    | 2         |                  | 28     |
| frect A,B             | fill rect from current pixel position to x A, y B                                                                                                              | 2         |                  | 29     |
| char A                | draw glyph assigned to hex code A at current pixel position                                                                                                    | 1         |                  | 2A     |
| charw A               | draw glyph assigned to hex code A at current pixel position, and update pixel position to reflect glyph width (including y position if at the edge of display) | 1         |                  | 2B     |
| mouse A,B             | place mouse x and y positions into addresses A and B                                                                                                           | 2         | WA WB            | 2C     |
| click A               | get click status and place into address A                                                                                                                      | 1         | WA               | 2D     |
| kb A                  | place current keyboard keycode into address A                                                                                                                  | 1         | WA               | 2E     |
| beep A                | play square wave at frequency A / 100 kHz                                                                                                                      | 1         |                  | 2F     |
| wait A                | pause execution for A milliseconds                                                                                                                             | 1         |                  | 30     |
| rnd A,B               | generate random number from 0 to B and place into A                                                                                                            | 2         | WA               | 31     |
| log A                 | log character A to console                                                                                                                                     | 1         |                  | 32     |
| halt                  | halt execution                                                                                                                                                 | 0         |                  | 33     |
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
- `02`: 2-bit mode
- `03`: 4-bit mode
- `04`: 8-bit mode
- `05`: 16-bit mode

## banks

`vonave` has two banks: one for general RAM, and another for file I/O.