# vonave assembler docs

the `vonave` assembler language is similar to most other assembler languages syntactically.

```
.graphics 2       ; set graphics mode to 2 (2-bit, 4 color palette) (default)
.width 64         ; set display width to 64 pixels (default)
.height 64        ; set display height to 64 pixels (default)
.bits 16          ; set bit width to 16 bits (default)

; including files is possible:
;
; .include "relative/path/to/file.vva"

def CHAR 'V       ; define global variable. characters with an apostrophe prefix are converted to their hex value (V -> 0x56)

mov 0, 86         ; move integer 86 into RAM address 0 (equivalent to 0x56)
mov 0, 0x56       ; move hex value 0x56 into RAM address 0
mov 0, CHAR       ; move variable CHAR's value into RAM address 0

log #0            ; print value at RAM address 0 to console (V)

label loop        ; define label loop
  inc 0           ; increment RAM address 0 by one
  cmp #0, 90      ; compare value at RAM address 0 to integer 90
  jne loop        ; jump to label loop if cmp argument A is not equal to B

halt              ; halt cpu
```

anything after a semicolon (`;`) is ignored, allowing for commenting.