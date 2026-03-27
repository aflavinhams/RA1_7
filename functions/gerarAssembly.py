'''
Ana Flávia Martins dos Santos (@aflavinhams)
Isabella Vanderlinde Berkembrock (@berkembrockisabella)
Michele Cristina Otta (@micheleotta)
Yejin Chung (@Chungyejin)

Grupo RA1_7
'''

def is_num(s):
    try:
        float(s) # tenta virar número
        return True
    except ValueError:
        return False

def is_float(s):
    return '.' in s # tem ponto = decimal

def criarState():
    # cria o "estado global" que vai ser compartilhado entre todas as linhas do arquivo
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
    # chamado no final — gera a seção .data com tudo que foi usado
    state["cod_assembly"].append("\n.data")

    # reserva espaço pra cada variável (ex: CONTADOR, MEM...)
    for var in state["variables"]:
        state["cod_assembly"].append(f"  addr_{var}: .word 0")

    # reserva espaço pra cada resultado de linha que foi salvo
    for label, is_float in state["result_lines"]:
        if is_float:
            state["cod_assembly"].append(f"  {label}: .float 0.0") # resultado decimal
        else:
            state["cod_assembly"].append(f"  {label}: .word 0") # resultado inteiro

    # declara os valores float usados no código (ex: 3.14, 1.6...)
    for value, label in state["float_constants"].items():
        state["cod_assembly"].append(f"  {label}: .float {value}")

    # junta tudo numa string e devolve o assembly completo
    return "\n".join(state["cod_assembly"])

def gerarMOD(r1, r2, cod_assembly, reg_count):
    # ARMv7 não tem instrução de resto (%), então:
    # quociente = r1 / r2
    # resto     = r1 - (quociente * r2)  ← isso é o que o MLS faz
    reg_quoc = f"r{reg_count[0]}" # registrador temporário pro quociente
    reg_count[0] += 1
    cod_assembly.append(f"  SDIV {reg_quoc}, {r1}, {r2}") # divide e guarda o quociente
    cod_assembly.append(f"  MLS {r1}, {reg_quoc}, {r2}, {r1}") # resto fica em r1

def gerarPOW(r1, r2, cod_assembly, reg_count, state):
    # ARMv7 não tem instrução de potência então é necessário loop:
    # começa com result = 1 e multiplica pela base r2 vezes
    pow_id = state["pow_count"] # id único pra esse loop não colidir com outros
    state["pow_count"] += 1

    reg_result = f"r{reg_count[0]}" # vai acumular o resultado
    reg_count[0] += 1
    reg_base = f"r{reg_count[0]}" # guarda a base original pra não perder durante o loop
    reg_count[0] += 1

    label_loop = f"pow_loop_{pow_id}" # label do início do loop
    label_end  = f"pow_end_{pow_id}"  # label do fim do loop

    cod_assembly.append(f"  MOV {reg_result}, #1")                           # result = 1
    cod_assembly.append(f"  MOV {reg_base}, {r1}")                           # salva a base
    cod_assembly.append(f"{label_loop}:")                                    # início do loop
    cod_assembly.append(f"  CMP {r2}, #0")                                   # expoente zerou?
    cod_assembly.append(f"  BEQ {label_end}")                                # sim → sai do loop
    cod_assembly.append(f"  MUL {reg_result}, {reg_result}, {reg_base}")     # result *= base
    cod_assembly.append(f"  SUB {r2}, {r2}, #1")                             # expoente--
    cod_assembly.append(f"  B {label_loop}")                                 # volta pro início
    cod_assembly.append(f"{label_end}:")                                     # fim do loop

    return reg_result # devolve o registrador com o resultado final

def floatParaInt(reg, cod_assembly, alloc_r):
    # converte um registrador VFP (S) pra inteiro (r)
    # necessário porque %, // e ^ só aceitam registradores r
    cod_assembly.append(f"  VCVT.S32.F32 {reg}, {reg}") # converte float pra int dentro do VFP
    novo_r = alloc_r() # aloca um registrador inteiro
    cod_assembly.append(f"  VMOV {novo_r}, {reg}") # move o valor convertido pro registrador r
    return novo_r # devolve o registrador inteiro com o valor

def gerarAssembly(tokens, state, linha_atual):
    stack = []  # pilha da linha: cada item é (nome_registrador, é_float?)

    # contadores em lista pra poder modificar dentro das funções auxiliares
    # resetam a cada linha pra nunca passar de r12
    reg_count  = [0] # próximo rX disponível
    vreg_count = [0] # próximo SX disponível

    # atalhos pro state pra não ficar repetindo state["..."] toda hora
    cod_assembly    = state["cod_assembly"]
    results         = state["results"]
    memory          = state["memory"]
    variables       = state["variables"]
    float_constants = state["float_constants"]

    def alloc_r():
        # pega o próximo registrador inteiro livre (r0, r1, r2...)
        r = f"r{reg_count[0]}"
        reg_count[0] += 1
        return r

    def alloc_s():
        # pega o próximo registrador VFP livre (S0, S1, S2...)
        s = f"S{vreg_count[0]}"
        vreg_count[0] += 1
        return s

    # mapeamento de operador → instrução assembly para inteiros
    int_operations = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "//": "SDIV", # divisão inteira com sinal
    }

    # mapeamento de operador → instrução assembly para floats (VFP)
    float_operations = {
        "+": "VADD.F32",
        "-": "VSUB.F32",
        "*": "VMUL.F32",
        "/": "VDIV.F32"
    }

    # conjunto de todos os operadores reconhecidos
    all_operations = set(int_operations.keys()) | {"/", "%", "^"}

    for i, token in enumerate(tokens):

        if is_num(token): # token é número
            if is_float(token): # decimal → vai pra registrador VFP (S)
                # verifica se esse valor já foi declarado antes pra não repetir no .data
                if token not in float_constants:
                    label = f"fconst_{state['float_const_count']}" # cria label novo
                    float_constants[token] = label # associa o valor ao label
                    state["float_const_count"] += 1
                else:
                    label = float_constants[token] # reutiliza label existente

                reg_addr = alloc_r() # registrador temporário só pro endereço
                s_reg    = alloc_s() # registrador que vai receber o float

                cod_assembly.append(f"  LDR {reg_addr}, ={label}") # carrega o endereço do float
                cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]") # busca o valor nesse endereço
                stack.append((s_reg, True)) # empilha como float

            else: # inteiro → MOV direto no registrador
                reg = alloc_r()
                cod_assembly.append(f"  MOV {reg}, #{token}") # copia o valor pro registrador
                stack.append((reg, False)) # empilha como inteiro

        elif token in all_operations: # token é operador
            # desempilha os dois operandos
            r2, r2_float = stack.pop()
            r1, r1_float = stack.pop()
            is_float_op = r1_float or r2_float # se qualquer um for float, a operação é float

            if token == "%": # resto → SDIV + MLS, só aceita registradores r
                # converte pra inteiro se vier de operação float
                if r1_float:
                    r1 = floatParaInt(r1, cod_assembly, alloc_r)
                if r2_float:
                    r2 = floatParaInt(r2, cod_assembly, alloc_r)
                gerarMOD(r1, r2, cod_assembly, reg_count)
                stack.append((r1, False)) # resto fica em r1 após o MLS

            elif token == "^": # potência → loop, só aceita registradores r
                # converte pra inteiro se vier de operação float
                if r1_float:
                    r1 = floatParaInt(r1, cod_assembly, alloc_r)
                if r2_float:
                    r2 = floatParaInt(r2, cod_assembly, alloc_r)
                reg_result = gerarPOW(r1, r2, cod_assembly, reg_count, state)
                stack.append((reg_result, False))

            elif token == "//": # divisão inteira → SDIV, só aceita registradores r
                # converte pra inteiro se vier de operação float
                if r1_float:
                    r1 = floatParaInt(r1, cod_assembly, alloc_r)
                if r2_float:
                    r2 = floatParaInt(r2, cod_assembly, alloc_r)
                cod_assembly.append(f"  SDIV {r1}, {r1}, {r2}") # divide e resultado fica em r1
                stack.append((r1, False))

            elif token == "/" or (is_float_op and token in float_operations): # operação com float → VFP
                if not r1_float: # r1 é inteiro, precisa converter pra float antes
                    s1 = alloc_s()
                    cod_assembly.append(f"  VMOV {s1}, {r1}") # copia os bits pro VFP
                    cod_assembly.append(f"  VCVT.F32.S32 {s1}, {s1}") # converte de int pra float
                else:
                    s1 = r1 # já é float, usa direto

                if not r2_float: # mesma coisa pra r2
                    s2 = alloc_s()
                    cod_assembly.append(f"  VMOV {s2}, {r2}")
                    cod_assembly.append(f"  VCVT.F32.S32 {s2}, {s2}")
                else:
                    s2 = r2

                s_res = alloc_s() # registrador pro resultado
                cod_assembly.append(f"  {float_operations[token]} {s_res}, {s1}, {s2}") # faz a operação
                stack.append((s_res, True)) # empilha resultado como float

            else: # ambos inteiros → instrução inteira normal
                cod_assembly.append(f"  {int_operations[token]} {r1}, {r1}, {r2}") # resultado fica em r1
                stack.append((r1, False))

        elif token.isalpha() and token.isupper() and token != "RES": # token é nome de variável
            var_name = token
            # token anterior é número ou ")" = armazenamento (ex: 5.0 MEM)
            if stack and (tokens[i-1] == ")" or is_num(tokens[i-1])):
                valor_reg, valor_float = stack.pop() # pega o valor que vai ser armazenado

                memory[var_name] = (f"addr_{var_name}", valor_float) # anota onde a variável fica

                if var_name not in variables:
                    variables.append(var_name) # marca pra reservar espaço no .data

                reg_addr = alloc_r()
                cod_assembly.append(f"  LDR {reg_addr}, =addr_{var_name}") # carrega endereço da variável

                if valor_float:
                    cod_assembly.append(f"  VSTR {valor_reg}, [{reg_addr}]") # salva float na memória
                else:
                    cod_assembly.append(f"  STR {valor_reg}, [{reg_addr}]") # salva inteiro na memória

            else: # token anterior não é valor = leitura (ex: MEM sozinho)
                if var_name in memory: # variável já existe
                    mem_label, stored_float = memory[var_name]
                    if stored_float: # é float → carrega com VLDR
                        reg_addr = alloc_r()
                        s_reg    = alloc_s()
                        cod_assembly.append(f"  LDR {reg_addr}, ={mem_label}") # endereço da variável
                        cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]") # busca o float
                        stack.append((s_reg, True))
                    else: # é inteiro → carrega com LDR
                        reg = alloc_r()
                        cod_assembly.append(f"  LDR {reg}, ={mem_label}") # endereço da variável
                        cod_assembly.append(f"  LDR {reg}, [{reg}]") # busca o inteiro
                        stack.append((reg, False))
                else: # variável não existe ainda → inicializa com 0
                    reg = alloc_r()
                    cod_assembly.append(f"  MOV {reg}, #0")
                    stack.append((reg, False))

        elif token == "RES": # token é o comando especial RES
            stack.pop() # descarta o registrador do N da pilha (só precisamos do valor numérico)
            n = int(tokens[i - 1]) # pega o N do token anterior
            linha_alvo = linha_atual - n # calcula qual linha buscar

            if linha_alvo not in results:
                raise Exception(f"RES fora do intervalo: linha {linha_alvo} não encontrada")

            mem_label, origem_float = results[linha_alvo] # acha onde o resultado foi salvo

            if origem_float: # resultado é float → carrega com VLDR
                reg_addr = alloc_r()
                s_reg    = alloc_s()
                cod_assembly.append(f"  LDR {reg_addr}, ={mem_label}") # endereço do resultado
                cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]") # busca o float
                stack.append((s_reg, True))
            else: # resultado é inteiro → carrega com LDR
                reg = alloc_r()
                cod_assembly.append(f"  LDR {reg}, ={mem_label}") # endereço do resultado
                cod_assembly.append(f"  LDR {reg}, [{reg}]") # busca o inteiro
                stack.append((reg, False))

    # salva resultado final da linha na memória pra RES acessar depois
    if stack:
        res_reg, res_float = stack[-1] # pega o topo da pilha = resultado da linha
        res_label = f"result_{linha_atual}" # label único pra esse resultado
        reg_addr  = alloc_r()

        cod_assembly.append(f"  LDR {reg_addr}, ={res_label}") # endereço onde vai salvar
        if res_float:
            cod_assembly.append(f"  VSTR {res_reg}, [{reg_addr}]") # salva float
        else:
            cod_assembly.append(f"  STR {res_reg}, [{reg_addr}]") # salva inteiro

        results[linha_atual] = (res_label, res_float) # anota pra o RES saber onde buscar
        state["result_lines"].append((res_label, res_float)) # marca pra reservar espaço no .data