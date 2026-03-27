.syntax unified
.arch_extension idiv
.global _start
_start:
  MOV r0, #3
  MOV r1, #9
  VMOV S0, r0
  VCVT.F32.S32 S0, S0
  VMOV S1, r1
  VCVT.F32.S32 S1, S1
  VDIV.F32 S2, S0, S1
  LDR r2, =addr_AIMY
  VSTR S2, [r2]
  MOV r0, #2
  MOV r1, #2
  MOV r2, #1
  MOV r3, r0
pow_loop_0:
  CMP r1, #0
  BEQ pow_end_0
  MUL r2, r2, r3
  SUB r1, r1, #1
  B pow_loop_0
pow_end_0:
  MOV r4, #5
  MOV r5, #10
  ADD r4, r4, r5
  ADD r2, r2, r4
  LDR r6, =result_2
  STR r2, [r6]
  MOV r0, #10
  MOV r1, #2
  SUB r0, r0, r1
  MOV r2, #50
  MOV r3, #5
  SDIV r2, r2, r3
  ADD r0, r0, r2
  MOV r4, #1
  LDR r5, =result_2
  LDR r5, [r5]
  MOV r6, #10
  SDIV r7, r5, r6
  MLS r5, r7, r6, r5
  ADD r0, r0, r5
  LDR r8, =result_3
  STR r0, [r8]
  LDR r0, =fconst_0
  VLDR S0, [r0]
  LDR r1, =fconst_1
  VLDR S1, [r1]
  VADD.F32 S2, S0, S1
  LDR r2, =fconst_2
  VLDR S3, [r2]
  LDR r3, =addr_ABC
  VSTR S3, [r3]
  LDR r4, =addr_ABC
  VLDR S4, [r4]
  VMUL.F32 S5, S2, S4
  LDR r5, =result_4
  VSTR S5, [r5]
  MOV r0, #10
  MOV r1, #3
  SDIV r2, r0, r1
  MLS r0, r2, r1, r0
  MOV r3, #3
  MOV r4, #1
  MOV r5, r0
pow_loop_1:
  CMP r3, #0
  BEQ pow_end_1
  MUL r4, r4, r5
  SUB r3, r3, #1
  B pow_loop_1
pow_end_1:
  LDR r6, =result_5
  STR r4, [r6]
  MOV r0, #1
  MOV r1, #11
  MOV r2, #2
  MUL r1, r1, r2
  ADD r0, r0, r1
  LDR r3, =result_6
  STR r0, [r3]
  MOV r0, #5
  LDR r1, =fconst_3
  VLDR S0, [r1]
  VMOV S1, r0
  VCVT.F32.S32 S1, S1
  VMUL.F32 S2, S1, S0
  MOV r2, #10
  LDR r3, =fconst_4
  VLDR S3, [r3]
  VMOV S4, r2
  VCVT.F32.S32 S4, S4
  VMUL.F32 S5, S4, S3
  VDIV.F32 S6, S2, S5
  LDR r4, =result_7
  VSTR S6, [r4]
  LDR r0, =addr_AIMY
  VLDR S0, [r0]
  MOV r1, #4
  VMOV S1, r1
  VCVT.F32.S32 S1, S1
  VADD.F32 S2, S0, S1
  LDR r2, =fconst_5
  VLDR S3, [r2]
  LDR r3, =fconst_6
  VLDR S4, [r3]
  VMUL.F32 S5, S3, S4
  VDIV.F32 S6, S2, S5
  LDR r4, =result_2
  VSTR S6, [r4]
  MOV r0, #90
  MOV r1, #2
  SDIV r0, r0, r1
  MOV r2, #5
  SDIV r3, r0, r2
  MLS r0, r3, r2, r0
  LDR r4, =result_9
  STR r0, [r4]
  MOV r0, #4
  LDR r1, =result_6
  LDR r1, [r1]
  MOV r2, #1
  LDR r3, =result_9
  LDR r3, [r3]
  ADD r1, r1, r3
  LDR r4, =result_10
  STR r1, [r4]

.data
  addr_AIMY: .word 0
  addr_ABC: .word 0
  result_2: .word 0
  result_3: .word 0
  result_4: .float 0.0
  result_5: .word 0
  result_6: .word 0
  result_7: .float 0.0
  result_8: .float 0.0
  result_9: .word 0
  result_10: .word 0
  fconst_0: .float 25.5
  fconst_1: .float 10.5
  fconst_2: .float 1.3
  fconst_3: .float 1.6
  fconst_4: .float 0.1
  fconst_5: .float 4.5
  fconst_6: .float 0.5
