.thumb

.equ TSAList, TimingList+4
.equ GraphicsList, TSAList+4
.equ PaletteList, GraphicsList+4
.equ SoundID, PaletteList+4

PUSH {r4-r7,lr}
MOV r7,r9
MOV r6,r8
PUSH {r6,r7}
MOV r4,r0
LDR r0, SkillAnimStruct
MOV r1,#3
LDR r2, InitializeStruct
BL goto_r2
MOV r7,r0
STR r4,[r7,#0x5c]
MOV r0,#0
STRH r0,[r7,#0x2c]
STR r0,[r7,#0x44]
LDR r0, TimingList
STR r0,[r7,#0x48]
LDR r0, TSAList
STR r0,[r7,#0x4c]
STR r0,[r7,#0x50]
LDR r0, GraphicsList
STR r0,[r7,#0x54]
LDR r0, PaletteList
STR r0,[r7,#0x58]
LDR r2, settransparency
BL goto_r2
LDR r0, BattleBuffer
MOV r1,#0
LDSH r0,[r0,r1]
CMP r0,#0
BEQ JumpTarget
LDR r0,[r7,#0x5c]
LDR r2, routine2
BL goto_r2
CMP r0,#0
BNE JumpTarget2
MOV r0,#1
MOV r1,#0x18
MOV r2,#0
LDR r3, routine3
BL goto_r3
B JumpTarget
JumpTarget2:
MOV r0,#1
MOV r1,#0xe8
MOV r2,#0
LDR r3, routine3
BL goto_r3
JumpTarget:
LDR r4,[r7,#0x5c]
LDR r2, const1
MOV r9,r2
MOV r0,r4
LDR r3, routine2
BL goto_r3
LSL r0,#3
ADD r0,r9
LDR r6,[r0]
MOV r0,r4
LDR r3, routine2
BL goto_r3
LSL r0,#1
ADD r0,#1
LSL r0,#2
ADD r0,r9
LDR r1,[r0]
LDRH r0,[r4,#0x10]
MOV r3,#0x20
MOV r8,r3
MOV r2,r8
ORR r0,r2
STRH r0,[r4,#0x10]
LDRH r0,[r4]
MOV r5, #8
ORR r0,r5
STRH r0,[r4]
LDRH r0,[r6,#0x10]
ORR r0,r2
STRH r0,[r6,#0x10]
LDRH r0,[r6]
ORR r0,r5
STRH r0,[r6]
LDRH r0,[r1,#0x10]
ORR r0,r2
STRH r0,[r1,#0x10]
LDRH r0,[r1]
ORR r0,r5
STRH r0,[r1]
LDR r0,[r7,#0x5c]
LDR r3, routine4
BL goto_r3
MOV r4,r0
LDR r3, routine2
BL goto_r3
LSL r0,#3
ADD r0,r9
LDR r6,[r0]
MOV r0,r4
LDR r3, routine2
BL goto_r3
LSL r0,#1
ADD r0,#1
LSL r0,#2
ADD r0,r9
LDR r1,[r0]
LDRH r0,[r4,#0x10]
MOV r3,r8
ORR r0,r3
STRH r0,[r4,#0x10]
LDRH r0,[r4]
ORR r0,r5
STRH r0,[r4]
LDRH r0,[r6,#0x10]
ORR r0,r3
STRH r0,[r6,#0x10]
LDRH r0,[r6]
ORR r0,r5
STRH r0,[r6]
LDRH r0,[r1,#0x10]
ORR r0,r3
STRH r0,[r1,#0x10]
LDRH r0,[r1]
ORR r5,r0
STRH r5,[r1]
LDR r0, SoundID
MOV r1, #0x80
LSL r1,#1
LDR r2,[r7,#0x5c]
MOV r3,#2
LDSH r2,[r2,r3]
MOV r3,#1
LDR r4, routine5
BL goto_r4
POP {r3,r4}
MOV r8,r3
MOV r9,r4
POP {r4-r7}
POP {r2}

goto_r2:
BX r2
goto_r3:
BX r3
goto_r4:
BX r4

.align
SkillAnimStruct:
.long 0x85d9318
BattleBuffer:
.long 0x203e120
const1:
.long 0x2000000
InitializeStruct:
.long 0x8002c7c|1
settransparency:
.long 0x80551b0|1
routine2:
.long 0x805a16c|1
routine3:
.long 0x800148c|1
routine4:
.long 0x805a2b4|1
routine5:
.long 0x80729a4|1
TimingList:
@POIN to table of frames and durations: XXXX YYYY where x is frame and y is duration (in this case labeled BG only)
@POIN TSAList
@POIN GraphicsList
@POIN PaletteList
@SHORT sfx
