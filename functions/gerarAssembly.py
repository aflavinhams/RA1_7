def is_num(s):
    try:
        float(s) # tenta virar número
        return True
    except ValueError:
        return False

def is_float(s):
    return '.' in s # tem ponto = decimal

def criarState():
    return {
        "cod_assembly": [
            ".syntax unified",       # sintaxe moderna
            ".arch_extension idiv",  # libera SDIV
            ".global _start",
            "_start:"
        ],
        "results": {},          # resultados salvos por linha
        "memory": {},           # variáveis salvas
        "variables": [],        # variáveis pra declarar no .data
        "result_lines": [],     # resultados pra declarar no .data
        "float_constants": {},  # floats já declarados
        "float_const_count": 0, # contador de floats
        "pow_count": 0          # contador de loops de potência
    }

def finalizarAssembly(state):
    state["cod_assembly"].append("\n.data")

    for var in state["variables"]:
        state["cod_assembly"].append(f"  addr_{var}: .word 0")

    for label, is_float in state["result_lines"]:
        if is_float:
            state["cod_assembly"].append(f"  {label}: .float 0.0")
        else:
            state["cod_assembly"].append(f"  {label}: .word 0")

    for value, label in state["float_constants"].items():
        state["cod_assembly"].append(f"  {label}: .float {value}")

    return "\n".join(state["cod_assembly"])

def gerarMOD(r1, r2, cod_assembly, reg_count):
    # resto = r1 - (r1/r2 * r2) via SDIV + MLS
    reg_quoc = f"r{reg_count[0]}"
    reg_count[0] += 1
    cod_assembly.append(f"  SDIV {reg_quoc}, {r1}, {r2}") # quociente
    cod_assembly.append(f"  MLS {r1}, {reg_quoc}, {r2}, {r1}") # resto fica em r1

def gerarPOW(r1, r2, cod_assembly, reg_count, state):
    # multiplica r1 por ele mesmo r2 vezes
    pow_id = state["pow_count"]
    state["pow_count"] += 1

    reg_result = f"r{reg_count[0]}" # acumula o resultado
    reg_count[0] += 1
    reg_base = f"r{reg_count[0]}" # guarda a base
    reg_count[0] += 1

    label_loop = f"pow_loop_{pow_id}"
    label_end  = f"pow_end_{pow_id}"

    cod_assembly.append(f"  MOV {reg_result}, #1")
    cod_assembly.append(f"  MOV {reg_base}, {r1}")
    cod_assembly.append(f"{label_loop}:")
    cod_assembly.append(f"  CMP {r2}, #0")           # expoente zerou?
    cod_assembly.append(f"  BEQ {label_end}")         # sim → sai
    cod_assembly.append(f"  MUL {reg_result}, {reg_result}, {reg_base}") # result *= base
    cod_assembly.append(f"  SUB {r2}, {r2}, #1")      # expoente--
    cod_assembly.append(f"  B {label_loop}")
    cod_assembly.append(f"{label_end}:")

    return reg_result

def gerarAssembly(tokens, state, linha_atual):
    stack = []  # pilha: (registrador, é_float?)

    reg_count  = [0] # próximo rX disponível
    vreg_count = [0] # próximo SX disponível

    cod_assembly    = state["cod_assembly"]
    results         = state["results"]
    memory          = state["memory"]
    variables       = state["variables"]
    float_constants = state["float_constants"]

    def alloc_r():
        r = f"r{reg_count[0]}"
        reg_count[0] += 1
        return r

    def alloc_s():
        s = f"S{vreg_count[0]}"
        vreg_count[0] += 1
        return s

    int_operations = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "//": "SDIV",
    }

    float_operations = {
        "+": "VADD.F32",
        "-": "VSUB.F32",
        "*": "VMUL.F32",
        "/": "VDIV.F32"
    }

    all_operations = set(int_operations.keys()) | {"/", "%", "^"}

    for i, token in enumerate(tokens):

        if is_num(token):
            if is_float(token): # decimal → registrador VFP
                if token not in float_constants:
                    label = f"fconst_{state['float_const_count']}"
                    float_constants[token] = label
                    state["float_const_count"] += 1
                else:
                    label = float_constants[token] # reutiliza label existente

                reg_addr = alloc_r()
                s_reg    = alloc_s()
                cod_assembly.append(f"  LDR {reg_addr}, ={label}") # endereço do float
                cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]") # carrega o valor
                stack.append((s_reg, True))

            else: # inteiro → MOV direto
                reg = alloc_r()
                cod_assembly.append(f"  MOV {reg}, #{token}")
                stack.append((reg, False))

        elif token in all_operations:
            r2, r2_float = stack.pop()
            r1, r1_float = stack.pop()
            is_float_op = r1_float or r2_float # basta um ser float

            if token == "%": # resto → SDIV + MLS
                gerarMOD(r1, r2, cod_assembly, reg_count)
                stack.append((r1, False))

            elif token == "^": # potência → loop
                reg_result = gerarPOW(r1, r2, cod_assembly, reg_count, state)
                stack.append((reg_result, False))

            elif token == "/" or (is_float_op and token in float_operations): # op float → VFP
                if not r1_float: # converte r1 pra float se precisar
                    s1 = alloc_s()
                    cod_assembly.append(f"  VMOV {s1}, {r1}")
                    cod_assembly.append(f"  VCVT.F32.S32 {s1}, {s1}")
                else:
                    s1 = r1

                if not r2_float: # converte r2 pra float se precisar
                    s2 = alloc_s()
                    cod_assembly.append(f"  VMOV {s2}, {r2}")
                    cod_assembly.append(f"  VCVT.F32.S32 {s2}, {s2}")
                else:
                    s2 = r2

                s_res = alloc_s()
                cod_assembly.append(f"  {float_operations[token]} {s_res}, {s1}, {s2}")
                stack.append((s_res, True))

            else: # op inteira → instrução normal
                cod_assembly.append(f"  {int_operations[token]} {r1}, {r1}, {r2}")
                stack.append((r1, False))

        elif token.isalpha() and token.isupper() and token != "RES":
            var_name = token
            if stack and (tokens[i-1] == ")" or is_num(tokens[i-1])): # armazenamento
                valor_reg, valor_float = stack.pop()
                memory[var_name] = (f"addr_{var_name}", valor_float)

                if var_name not in variables:
                    variables.append(var_name)

                reg_addr = alloc_r()
                cod_assembly.append(f"  LDR {reg_addr}, =addr_{var_name}")

                if valor_float:
                    cod_assembly.append(f"  VSTR {valor_reg}, [{reg_addr}]")
                else:
                    cod_assembly.append(f"  STR {valor_reg}, [{reg_addr}]")

            else: # leitura
                if var_name in memory:
                    mem_label, stored_float = memory[var_name]
                    if stored_float:
                        reg_addr = alloc_r()
                        s_reg    = alloc_s()
                        cod_assembly.append(f"  LDR {reg_addr}, ={mem_label}")
                        cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]")
                        stack.append((s_reg, True))
                    else:
                        reg = alloc_r()
                        cod_assembly.append(f"  LDR {reg}, ={mem_label}")
                        cod_assembly.append(f"  LDR {reg}, [{reg}]")
                        stack.append((reg, False))
                else: # variável não existe → 0
                    reg = alloc_r()
                    cod_assembly.append(f"  MOV {reg}, #0")
                    stack.append((reg, False))

        elif token == "RES":
            stack.pop() # descarta o N da pilha
            n = int(tokens[i - 1])
            linha_alvo = linha_atual - n

            if linha_alvo not in results:
                raise Exception(f"RES fora do intervalo: linha {linha_alvo} não encontrada")

            mem_label, origem_float = results[linha_alvo]

            if origem_float:
                reg_addr = alloc_r()
                s_reg    = alloc_s()
                cod_assembly.append(f"  LDR {reg_addr}, ={mem_label}")
                cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]")
                stack.append((s_reg, True))
            else:
                reg = alloc_r()
                cod_assembly.append(f"  LDR {reg}, ={mem_label}")
                cod_assembly.append(f"  LDR {reg}, [{reg}]")
                stack.append((reg, False))

    # salva resultado final da linha na memória pra RES acessar depois
    if stack:
        res_reg, res_float = stack[-1]
        res_label = f"result_{linha_atual}"
        reg_addr  = alloc_r()

        cod_assembly.append(f"  LDR {reg_addr}, ={res_label}")
        if res_float:
            cod_assembly.append(f"  VSTR {res_reg}, [{reg_addr}]")
        else:
            cod_assembly.append(f"  STR {res_reg}, [{reg_addr}]")

        results[linha_atual] = (res_label, res_float)
        state["result_lines"].append((res_label, res_float))