'''
Ana Flávia Martins dos Santos (@aflavinhams)
Isabella Vanderlinde Berkembrock (@berkembrockisabella)
Michele Cristina Otta (@micheleotta)
Yejin Chung (@Chungyejin)

Grupo RA1_7
'''

from functions.gerarAssembly import is_num

# Função executarExpressao: validar o código Assembly que será gerado posteriormente
def executarExpressao(tokens: list[str], memoria: dict[str, float], resultados: dict[int, float], linha_atual: int):
    # Conjunto de operações
    operacoes = {"+", "-", "*", "/", "//", "%", "^"}
    # Pilha para avaliar expressões RPN
    stack = []
    
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
            case "//": # divisão inteira
                return (num1 // num2)
            case "%": # resto da divisão inteira
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
            resultado = operation(num1, num2, token) # Realiza a operação
            # Empilha o resultado
            stack.append(resultado)
        
        # Operação RES
        # (N RES): retorna resultado da expressão N linhas anteriores
        elif token == "RES":
            if stack:
                n = int(stack.pop())
                # N é um inteiro não negativo
                if n > 0 and (linha_atual - n) in resultados:
                    res = resultados[linha_atual - n]
                    stack.append(res)

        # Operação MEM
        # MEM pode ser qualquer conjunto de letras maiúsculas!
        elif token.isalpha() and token.isupper():
            # (V MEM): armazena valor em uma memória
            # Confere se tem um valor na pilha para ser armazenado
            # E se o token anterior a ele é um número ou resultado de uma operação
            # Exemplos: (1 MEM) ou ainda ((1 1 +) MEM)
            if stack and (tokens[i-1] == ")" or is_num(tokens[i-1])):
                v = stack.pop()
                memoria[token] = v # Atualiza a memória
            # (MEM): retorna o valor armazenado em MEM
            else:
                if token in memoria:
                    stack.append(memoria[token])
                else:
                    stack.append(0.0)
    
    # Atualiza histórico de resultados
    if stack: # Verificação pois o comando (V MEM) apenas armazena na memória, não retorna resultado!
        resultados[linha_atual] = stack.pop()
        
# Função de teste para validar a execução de expressões e comandos especiais
def testes_executarExpressao():
    testes =[
        ['(', '3.14', '2.0', '+', ')'],
        ['1', 'RES'],
        ['(', '(', '1.5', '2.0', '*', ')', '(', '3.0', '4.0', '*', ')', '/', ')'],
        ['(', '5.0', 'MEM', ')'],
        ['(', '2', 'RES', ')'],
        ['(', '10.5', 'CONTADOR', ')', 'CONTADOR'],
        ["(", "15.5", "4.2", "*", ")", "(", "10", "5", "+", ")", "/"],
        ["(", "10", "2", "^", ")", "(", "50", "5", "//", ")", "(", "1", "RES", "10", "%", ")", "+", "+"],
        ["(", "25.5", "10.5", "+", ")", "(", "3.14", "MI", "MI", ")", "*"],
        ["(", "(", "8", "2", "/", ")", "(", "3", "1", "-", ")", "*", ")", "(", "100", "50", "%", ")", "+"],
        ["100", "(", "(", "5", "2", "%", ")", "(", "10", "2", "*", ")", "+", ")", "/"],
        ['(', '10.5', 'MI', ')', 'MI'],
        ['(', '(', '3', '9', '/' ,')', 'ANA', ')'],
        ['(', '(', '2', '2', '^', ')', '(', '5', '10', '+', ')', '+', ')', 'ISA'],
        ['(', '5', '(', 'MI', ')', '+', ')']
        ]

    # Contador da linha atual da expressão
    linha = 1
    # Estrutura de dicionário para gerenciar múltiplas variáveis na memória
    memoria = {}
    # Dicionário de histórico de resultados para exibirResultados
    # Estrutura -> 'número de linha': 'resultado'
    # Para lidar corretamente com a operação RES, considerando casos da operação MEM que não salva no histórico de resultados!
    resultados = {}

    for teste in testes:
        executarExpressao(teste, memoria, resultados, linha)
        linha += 1
    print(resultados)
    print(memoria)