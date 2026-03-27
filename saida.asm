.syntax unified
.arch_extension idiv
.global _start
_start:

  LDR r0, =fconst_0
  VLDR S0, [r0]
  LDR r1, =fconst_1
  VLDR S1, [r1]
  VADD.F32 S2, S0, S1
  LDR r2, =fconst_2
  VLDR S3, [r2]
  VSUB.F32 S4, S2, S3
  LDR r3, =result_1
  VSTR S4, [r3]
  LDR r0, =fconst_3
  VLDR S0, [r0]
  LDR r1, =fconst_1
  VLDR S1, [r1]
  VMUL.F32 S2, S0, S1
  LDR r2, =fconst_4
  VLDR S3, [r2]
  LDR r3, =fconst_5
  VLDR S4, [r3]
  VMUL.F32 S5, S3, S4
  VDIV.F32 S6, S2, S5
  LDR r4, =result_2
  VSTR S6, [r4]
  LDR r0, =fconst_3
  VLDR S0, [r0]
  LDR r1, =fconst_1
  VLDR S1, [r1]
  VMUL.F32 S2, S0, S1
  MOV r2, #2
  SDIV r3, S2, r2
  MLS S2, r3, r2, S2
  LDR r4, =result_3
  STR S2, [r4]
  LDR r0, =fconst_3
  VLDR S0, [r0]
  LDR r1, =fconst_1
  VLDR S1, [r1]
  VMUL.F32 S2, S0, S1
  MOV r2, #2
  SDIV S2, S2, r2
  LDR r3, =result_4
  STR S2, [r3]
  LDR r0, =fconst_4
  VLDR S0, [r0]
  LDR r1, =fconst_5
  VLDR S1, [r1]
  VMUL.F32 S2, S0, S1
  MOV r2, #0
  MOV r3, #1
  MOV r4, S2
pow_loop_0:
  CMP r2, #0
  BEQ pow_end_0
  MUL r3, r3, r4
  SUB r2, r2, #1
  B pow_loop_0
pow_end_0:
  LDR r5, =result_5
  STR r3, [r5]
  LDR r0, =fconst_6
  VLDR S0, [r0]
  LDR r1, =addr_Z
  VSTR S0, [r1]
  LDR r2, =addr_Z
  VLDR S1, [r2]
  LDR r3, =result_6
  VSTR S1, [r3]
  MOV r0, #2
  LDR r1, =result_5
  LDR r1, [r1]
  MOV r2, #11
  MUL r1, r1, r2
  LDR r3, =result_7
  STR r1, [r3]
  LDR r0, =addr_Z
  VLDR S0, [r0]
  LDR r1, =addr_P
  VSTR S0, [r1]
  MOV r0, #3
  MOV r1, #4
  ADD r0, r0, r1
  LDR r2, =fconst_6
  VLDR S0, [r2]
  VMOV S1, r0
  VCVT.F32.S32 S1, S1
  VMUL.F32 S2, S1, S0
  LDR r3, =result_9
  VSTR S2, [r3]
  LDR r0, =fconst_7
  VLDR S0, [r0]
  LDR r1, =fconst_8
  VLDR S1, [r1]
  LDR r2, =fconst_9
  VLDR S2, [r2]
  VSUB.F32 S3, S1, S2
  VADD.F32 S4, S0, S3

  addr_Z: .word 0
  addr_P: .word 0
  result_1: .float 0.0
  result_2: .float 0.0
  result_3: .word 0
  result_4: .word 0
  result_5: .word 0
  result_6: .float 0.0
  result_7: .word 0
  result_9: .float 0.0
  result_10: .float 0.0
  fconst_0: .float 3.14
  fconst_1: .float 2.0
  fconst_2: .float 4.14
  fconst_3: .float 1.5
  fconst_4: .float 3.0
  fconst_5: .float 4.0
  fconst_6: .float 5.0
  fconst_7: .float 8.8
  fconst_8: .float 9.9
  fconst_9: .float 1.2
