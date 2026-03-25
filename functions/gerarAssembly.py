def is_num(s):
    try:
        float(s) # caso seja possível transformar o caractere em float, é um número
        return True
    except ValueError:
        return False

def is_float(s):
    # verifica se o número possui parte decimal (ponto flutuante)
    return '.' in s

def gerarAssembly(tokens, cod_assembly=[".global _start\n_start:"]):
    stack = []  # pilha — cada item é uma tupla (registrador, is_float)
    memory = {}  # memória para valores — cada item é (registrador, is_float)
    results = []  # lista de resultados — cada item é uma tupla (registrador, is_float)
    variables = []  # lista de variáveis declaradas (para gerar seção .data)
    float_constants = {}  # dicionário de constantes float → label (para gerar seção .data)
    float_const_count = 0  # contador para criação de labels de constantes float

    # operações inteiras e seus correspondentes em assembly
    int_operations = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "//": "SDIV",   # divisão inteira com sinal
        "//u": "UDIV",  # divisão inteira sem sinal
        "%": "MOD",
        "^": "POW"
    }

    # operações equivalentes em VFP para floats (NEON excluído no CPUlator)
    float_operations = {
        "+": "VADD.F32",
        "-": "VSUB.F32",
        "*": "VMUL.F32",
        "/": "VDIV.F32"
    }

    all_operations = set(int_operations.keys()) | {"/"}

    reg_count = 0   # contador para registradores inteiros (R0, R1, ...)
    vreg_count = 0  # contador para registradores VFP (S0, S1, ...)

    for i, token in enumerate(tokens):

        if is_num(token): # se o token for um número
            if is_float(token): # número float → carrega em registrador VFP (S)
                # reutiliza o label se a constante já foi declarada
                if token not in float_constants:
                    label = f"fconst_{float_const_count}" # cria um label para a constante float
                    float_constants[token] = label # associa o valor ao label
                    float_const_count += 1 # incrementa o contador de constantes float
                else:
                    label = float_constants[token] # reutiliza o label existente

                reg_addr = f"R{reg_count}" # registrador temporário para o endereço
                reg_count += 1 # incrementa o contador de registradores inteiros
                s_reg = f"S{vreg_count}" # registrador VFP para o valor float
                vreg_count += 1 # incrementa o contador de registradores VFP

                cod_assembly.append(f"  LDR {reg_addr}, ={label}") # carrega o endereço da constante
                cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]") # carrega o valor float do endereço

                stack.append((s_reg, True)) # empilha o registrador VFP como float

            else: # número inteiro → carrega em registrador inteiro (R)
                reg = f"R{reg_count}" # cria um novo registrador inteiro
                cod_assembly.append(f"  MOV {reg}, #{token}") # copia o número para o registrador criado
                stack.append((reg, False)) # empilha o registrador inteiro
                reg_count += 1 # incrementa o contador de registradores inteiros

        elif token in all_operations: # se o token for um operador
            # desempilha dois operandos
            r2, r2_float = stack.pop()
            r1, r1_float = stack.pop()

            is_float_op = r1_float or r2_float # operação é float se qualquer operando for float

            if token == "/" or (is_float_op and token in float_operations): # operação com floats → usa VFP
                # converte r1 para registrador VFP se ainda for inteiro
                if not r1_float:
                    s1 = f"S{vreg_count}"
                    vreg_count += 1 # incrementa o contador de registradores VFP
                    cod_assembly.append(f"  VMOV {s1}, {r1}") # move inteiro para VFP
                    cod_assembly.append(f"  VCVT.F32.S32 {s1}, {s1}") # converte para float
                else:
                    s1 = r1 # já é registrador VFP

                # converte r2 para registrador VFP se ainda for inteiro
                if not r2_float:
                    s2 = f"S{vreg_count}"
                    vreg_count += 1 # incrementa o contador de registradores VFP
                    cod_assembly.append(f"  VMOV {s2}, {r2}") # move inteiro para VFP
                    cod_assembly.append(f"  VCVT.F32.S32 {s2}, {s2}") # converte para float
                else:
                    s2 = r2 # já é registrador VFP

                vfp_op = float_operations[token] # instrução VFP correspondente
                s_res = f"S{vreg_count}" # registrador VFP para o resultado
                vreg_count += 1 # incrementa o contador de registradores VFP

                cod_assembly.append(f"  {vfp_op} {s_res}, {s1}, {s2}") # realiza a operação VFP

                stack.append((s_res, True)) # empilha o resultado como float
                results.append((s_res, True)) # armazena o resultado

            else: # ambos inteiros → usa instruções inteiras (ADD, SUB, MUL, SDIV, UDIV...)
                int_op = int_operations[token] # instrução inteira correspondente
                cod_assembly.append(f"  {int_op} {r1}, {r1}, {r2}") # realiza a operação inteira e atualiza o último registrador desempilhado com o resultado
                stack.append((r1, False)) # empilha o resultado como inteiro
                results.append((r1, False)) # armazena o resultado

        elif token.isalpha() and token.isupper() and token != "RES": # caso queira armazenar um valor em uma variável
            var_name = token # nome da variável
            valor_reg, valor_float = stack.pop() # desempilha o registrador do valor da pilha

            memory[var_name] = (valor_reg, valor_float) # armazena na memória com tipo

            if var_name not in variables: # registra a variável para gerar a seção .data
                variables.append(var_name)

            reg_addr = f"R{reg_count}" # registrador temporário para o endereço
            reg_count += 1 # incrementa o contador de registradores inteiros
            cod_assembly.append(f"  LDR {reg_addr}, =addr_{var_name}") # carrega o endereço da variável

            if valor_float: # valor float → usa VSTR para armazenar registrador VFP
                cod_assembly.append(f"  VSTR {valor_reg}, [{reg_addr}]") # armazena float no endereço
            else: # valor inteiro → usa STR para armazenar registrador inteiro
                cod_assembly.append(f"  STR {valor_reg}, [{reg_addr}]") # armazena inteiro no endereço

        elif token == "RES": # caso seja o comando especial "RES"
            print(f"Results: {results}")
            n = int(tokens[i - 1]) # pega o valor de N

            if n < len(results):
                reg_origem, origem_float = results[-(n + 1)] # volta N resultados e pega o registrador do resultado
            else:
                raise Exception("RES fora do intervalo")

            if origem_float: # resultado é float → copia entre registradores VFP
                new_reg = f"S{vreg_count}"
                vreg_count += 1 # incrementa o contador de registradores VFP
                cod_assembly.append(f"  VMOV {new_reg}, {reg_origem}") # copia o valor float recuperado
                stack.append((new_reg, True)) # empilha como float
            else: # resultado é inteiro → copia entre registradores inteiros
                new_reg = f"R{reg_count}"
                reg_count += 1 # incrementa o contador de registradores inteiros
                cod_assembly.append(f"  MOV {new_reg}, {reg_origem}") # copia o valor inteiro recuperado
                stack.append((new_reg, False)) # empilha como inteiro

        elif token.isalpha(): # caso seja qualquer token alfabético → carrega o valor da memória para um registrador
            if token in memory: # se a variável existir
                stored_reg, stored_float = memory[token] # recupera o tipo do valor armazenado

                if stored_float: # variável float → carrega com VLDR para registrador VFP
                    reg_addr = f"R{reg_count}"
                    reg_count += 1 # incrementa o contador de registradores inteiros
                    s_reg = f"S{vreg_count}"
                    vreg_count += 1 # incrementa o contador de registradores VFP
                    cod_assembly.append(f"  LDR {reg_addr}, =addr_{token}") # carrega o endereço da variável
                    cod_assembly.append(f"  VLDR {s_reg}, [{reg_addr}]") # carrega o valor float do endereço
                    stack.append((s_reg, True)) # empilha como float
                else: # variável inteira → carrega com LDR para registrador inteiro
                    reg = f"R{reg_count}"
                    reg_count += 1 # incrementa o contador de registradores inteiros
                    cod_assembly.append(f"  LDR {reg}, =addr_{token}") # carrega o endereço da variável
                    cod_assembly.append(f"  LDR {reg}, [{reg}]") # carrega o valor inteiro do endereço
                    stack.append((reg, False)) # empilha como inteiro

            else: # caso a variável não existir → inicializa com 0 inteiro
                reg = f"R{reg_count}"
                reg_count += 1 # incrementa o contador de registradores inteiros
                cod_assembly.append(f"  MOV {reg}, #0") # copia o valor 0 para a variável
                stack.append((reg, False)) # empilha como inteiro

    # gera a seção .data com variáveis e constantes float declaradas
    cod_assembly.append("\n.data")
    for var in variables:
        cod_assembly.append(f"  addr_{var}: .word 0") # reserva espaço para cada variável inteira
    for value, label in float_constants.items():
        cod_assembly.append(f"  {label}: .float {value}") # declara cada constante float com seu label

    return "\n".join(cod_assembly) # retorna a lista de códigos assembly como uma string única