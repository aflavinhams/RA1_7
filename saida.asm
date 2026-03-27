.syntax unified
.arch_extension idiv
.global _start
_start:
  MOV r0, #1
  MOV r1, #2
  ADD r0, r0, r1
  LDR r2, =fconst_0
  VLDR S0, [r2]
  VMOV S1, r0
  VCVT.F32.S32 S1, S1
  VADD.F32 S2, S1, S0
  LDR r3, =result_1
  VSTR S2, [r3]
  LDR r0, =fconst_1
  VLDR S0, [r0]
  LDR r1, =fconst_2
  VLDR S1, [r1]
  VSUB.F32 S2, S0, S1
  LDR r2, =addr_SS
  VSTR S2, [r2]
  LDR r0, =fconst_3
  VLDR S0, [r0]
  MOV r1, #2
  LDR r2, =result_1
  VLDR S1, [r2]
  VMUL.F32 S2, S0, S1
  LDR r3, =result_3
  VSTR S2, [r3]
  MOV r0, #1
  LDR r1, =result_3
  VLDR S0, [r1]
  MOV r2, #121
  MOV r3, #11
  VMOV S1, r2
  VCVT.F32.S32 S1, S1
  VMOV S2, r3
  VCVT.F32.S32 S2, S2
  VDIV.F32 S3, S1, S2
  MOV r4, #1
  MOV r5, S0
pow_loop_0:
  CMP S3, #0
  BEQ pow_end_0
  MUL r4, r4, r5
  SUB S3, S3, #1
  B pow_loop_0
pow_end_0:
  LDR r6, =result_4
  STR r4, [r6]
  MOV r0, #81
  MOV r1, #7
  SDIV r2, r0, r1
  MLS r0, r2, r1, r0
  LDR r3, =addr_SS
  VLDR S0, [r3]
  VMOV S1, r0
  VCVT.F32.S32 S1, S1
  VADD.F32 S2, S1, S0
  LDR r4, =result_5
  VSTR S2, [r4]
  MOV r0, #10
  MOV r1, #9
  SDIV r0, r0, r1
  LDR r2, =addr_NOVO
  STR r0, [r2]
  MOV r0, #0
  LDR r1, =fconst_4
  VLDR S0, [r1]
  VMOV S1, r0
  VCVT.F32.S32 S1, S1
  VADD.F32 S2, S1, S0
  LDR r2, =result_7
  VSTR S2, [r2]
  LDR r0, =fconst_5
  VLDR S0, [r0]
  LDR r1, =fconst_6
  VLDR S1, [r1]
  VMUL.F32 S2, S0, S1
  LDR r2, =fconst_7
  VLDR S3, [r2]
  LDR r3, =fconst_8
  VLDR S4, [r3]
  VMUL.F32 S5, S3, S4
  VDIV.F32 S6, S2, S5
  LDR r4, =result_8
  VSTR S6, [r4]
  LDR r0, =fconst_9
  VLDR S0, [r0]
  LDR r1, =fconst_7
  VLDR S1, [r1]
  VMUL.F32 S2, S0, S1
  MOV r2, #4
  SDIV r3, S2, r2
  MLS S2, r3, r2, S2
  LDR r4, =result_9
  STR S2, [r4]
  LDR r0, =fconst_10
  VLDR S0, [r0]
  MOV r1, #3
  VMOV S1, r1
  VCVT.F32.S32 S1, S1
  VADD.F32 S2, S0, S1
  LDR r2, =fconst_11
  VLDR S3, [r2]
  VMUL.F32 S4, S2, S3
  LDR r3, =result_10
  VSTR S4, [r3]

.data
  addr_SS: .word 0
  addr_NOVO: .word 0
  result_1: .float 0.0
  result_3: .float 0.0
  result_4: .word 0
  result_5: .float 0.0
  result_7: .float 0.0
  result_8: .float 0.0
  result_9: .word 0
  result_10: .float 0.0
  fconst_0: .float 3.5
  fconst_1: .float 9.7
  fconst_2: .float 1.3
  fconst_3: .float 1.5
  fconst_4: .float 13.3
  fconst_5: .float 3.0
  fconst_6: .float 4.0
  fconst_7: .float 2.0
  fconst_8: .float 6.0
  fconst_9: .float 7.5
  fconst_10: .float 3.14
  fconst_11: .float 2.5