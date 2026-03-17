def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def gerarAssembly(tokens):
    cod_assembly = [f".global _start\n_start:"]
    stack = []
    operations = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "SDIV", "%": "MOD", "^": "POW"}
    reg_count = 0

    for token in tokens: 

        if is_num(token): #se o token for um número
            reg = f"R{reg_count}" #cria um novo registrador
            cod_assembly.append(f"  MOV {reg}, #{token}") # carrega número
            stack.append(reg) # empilha o número na pilha
            reg_count +=1 # encrementa o contador de registradores

        elif token in operations.keys(): # caso for uma operação
            r2 = stack.pop() # desempilha o primeiro número
            r1 = stack.pop() # desempilha o segundo número
            op_ass = operations[token]

            cod_assembly.append(f"  {op_ass} {r1}, {r1}, {r2}") # aplica em assembly a operação respectiva aos números
            stack.append(r1) # empilha o resultado

    return "\n".join(cod_assembly)

print(gerarAssembly(["3", "4", "+", "2", "*"]))