# Criar um método, antes do Autômato Finito Determinístico, para lidar com parênteses aninhados.
# 1 EXPRESSÃO POR LINHA

def executarExpressao(tokens):
    
    # estrutura de dicionário para gerenciar múltiplas variáveis na memória
    memoria = {}
    linha_atual = 1
    # vetor de resultados para exibirResultados
    resultados = []
    
    # (N RES): retorna resultado da expressão N linhas anteriores
    def get_res(n_linhas):
        # N é um inteiro não negativo
        if n_linhas > 0 and int: #???
            return memoria[n_linhas] # ir armazenando o resultado de cada linha, coloca nome o numero mesmo
    
    # (V MEM): armazena valor em uma memória
    # MEM pode ser qualquer conjunto de letras maiúsculas
    def store_mem(valor, mem):
        memoria[mem] = valor
    
    # (MEM): retorna o valor armazenado em MEM
    def get_mem(mem):
        if memoria[mem]:
            return memoria[mem]
        # se memoria não inicializada, retorna 0.0
        return 0.0
    
    # PILHA avaliar expressões RPN
    # Implementar operações (+, -, *, /, %, ^) com precisão de 64 bits (IEEE 754) -> aparentemente float ja da conta, investigar mesmo
    def operation(num1, num2, type):
        match type:
            case "+":
                return (num1 + num2)
            case "-":
                # qual a ordem??? A- B ou B - A? tem numero ja negativo?
                return (num1 - num2)
            case "*":
                return (num1 * num2)
            case "/":
                return (num1 / num2)
            case "//": # para inteiros ??????
                return (num1 // num2)
            case "%":
                return (num1 % num2)
            case "^":
                return (num1 ** num2)
    
    
    # atualiza RESULTADOS e MEMORIA
    
    
    
    return resultados


# Gerenciar a memória MEM para comandos (V MEM) e (MEM);
# histórico de resultados (?)

ex_tokens = ['(', '3.14', '2.0', '+', ')']