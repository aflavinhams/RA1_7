def is_num(s):
    try:
        float(s) # caso seja possível transformar o caractere em float, é um número
        return True
    except ValueError:
        return False

def gerarAssembly(tokens, cod_assembly=[".global _start\n_start:"]):
    stack = [] # pilha
    memory = {} # memória para valores
    results = [] # lista de resultados
    operations = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "SDIV", "%": "MOD", "^": "POW"} # operações -> caractere : operação assembly correspondente
    reg_count = 0 # contador para criação de registradores

    for i, token in enumerate(tokens):

        if is_num(token): # se o token for um número
            reg = f"R{reg_count}" # cria um novo registrador
            cod_assembly.append(f"  MOV {reg}, #{token}") # copia o número para o registrador criado
            stack.append(reg) # empilha o registrador
            reg_count += 1 # incrementa o contador de registradores

        elif token in operations: # se o token for um operador
            # desempilha dois operandos
            r2 = stack.pop()
            r1 = stack.pop()

            cod_assembly.append(f"  {operations[token]} {r1}, {r1}, {r2}") # realiza a operação correspondente e atualiza o último registrador desempilhado com o resultado da operação

            stack.append(r1) # empilha o último registrador
            results.append(r1) # armazena o resultado

        elif token.isalpha() and token.isupper() and token != "RES": # caso queira armazenar um valor em uma variáve;
            var_name = token # nome da variável
            valor_reg = stack.pop() # desempilha o registrador do valor da pilha

            memory[var_name] = valor_reg # armazena na memória
            cod_assembly.append(f"  STR {valor_reg}, ={var_name}") # gera o código que armazena o nome da variável

        elif token == "RES": # caso seja o comando especial "RES"
            print(f"Results: {results}")
            n = int(tokens[i - 1]) # pega o valor de N

            if n < len(results):
                reg_origem = results[-(n+1)] # volta N resultados e pega o registrador do resultado
            else:
                raise Exception("RES fora do intervalo")

            reg = f"R{reg_count}" # cria um novo registrador
            cod_assembly.append(f"  MOV {reg}, {reg_origem}") # copia o valor da resposta recuperada no novo registrador

            stack.append(reg) # empilha o registrador
            reg_count += 1 # incrementa o registrador

        elif token.isalpha():  # caso seja qualquer token alfabético -> carrega o valor da memória para um registrador
            if token in memory: # se a variável existir
                reg = f"R{reg_count}" # cria um novo registrador
                cod_assembly.append(f"  LDR {reg}, ={token}") # carrega o valor do registrador da variável
            else: # caso não existir
                reg = f"R{reg_count}"
                cod_assembly.append(f"  MOV {reg}, #0.0") # copia o valor 0.0 para a variável

            stack.append(reg) # empilha o registrador
            reg_count += 1 # incrementa o registrador

    return "\n".join(cod_assembly) # retorna a lista de códigos assembly como uma string única