# Função do gerarAssembly (copia de gerarAssembly, apagar depois)
def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def executarExpressao(tokens):
    
    # Conjunto de operações
    operacoes = {"+", "-", "*", "/", "//", "%", "^"}
    # Pilha para avaliar expressões RPN
    stack = []
    # Estrutura de dicionário para gerenciar múltiplas variáveis na memória
    memoria = {}
    # Vetor de histórico de resultados para exibirResultados
    resultados = []
    
    # Implementar operações (+, -, *, /, %, ^) com precisão de 64 bits (IEEE 754)
    def operation(num1, num2, type):
        match type:
            case "+":
                return (num1 + num2)
            case "-":
                return (num1 - num2)
            case "*":
                return (num1 * num2)
            case "/":
                return (num1 / num2)
            case "//":
                return (num1 // num2)
            case "%":
                return (num1 % num2)
            case "^":
                return (num1 ** num2)
    
    # Percorre cada token para executar as expressões
    for i, token in enumerate(tokens):
        
        # Se token for Número
        if is_num(token):
            stack.append(float(token)) # Empilha o número na pilha

        # Se token for Operacao
        elif token in operacoes:
            num2 = stack.pop() # Desempilha o primeiro número
            num1 = stack.pop() # Desempilha o segundo número
            resultado = operation(num1, num2, token)
            # Empilha o resultado
            stack.append(resultado)
        
        # Operação RES
        # (N RES): retorna resultado da expressão N linhas anteriores
        elif token == "RES":
            if stack:
                n = int(stack.pop())
                # N é um inteiro não negativo
                if n > 0 and n < len(resultados): # and int ???
                    res = resultados[-(n+1)]
                    # resultados.append(res) # ir armazenando o resultado de cada linha
                    stack.append(res)

        # Operação MEM
        # MEM pode ser qualquer conjunto de letras maiúsculas!
        elif token.isalpha() and token.isupper():
            # (V MEM): armazena valor em uma memória
            if i > 0 and is_num(tokens[i-1]): # revisar
                v = stack.pop()
                memoria[token] = v
            # (MEM): retorna o valor armazenado em MEM
            else:
                if token in memoria:
                    stack.append(memoria[token])
                else:
                    stack.append(0.0)
    
    # fazer historico de resultados
    return stack


# testes
ex_tokens = ['(', '3.14', '2.0', '+', ')']
ex_tokens = ['(', '(', '1.5', '2.0', '*', ')', '(', '3.0', '4.0', '*', ')', '/', ')']
ex_tokens = ['(', '5.0', 'MEM', ')']
ex_tokens = ['(', '2', 'RES', ')']
ex_tokens = ['(', '10.5', 'CONTADOR', ')', 'CONTADOR']
print(executarExpressao(ex_tokens))