from functions.lerArquivo import ler_arquivo
from functions.parseexpressao import parseExpressao
from functions.gerarAssembly import gerarAssembly, criarState, finalizarAssembly
from functions.exibirResultados import exibirResultados
from functions.executarExpressao import executarExpressao

print(f"Arquivo: {ler_arquivo('arquivosTeste/teste2.txt')}\n")
arq = ler_arquivo("arquivosTeste/teste2.txt")

memoria = {}
resultados_py = {}
linha = 1

state = criarState()  # cria o estado compartilhado entre todas as linhas

for line in arq:
    line_tokens = parseExpressao(line)
    print(line_tokens)

    executarExpressao(line_tokens, memoria, resultados_py, linha)
    gerarAssembly(line_tokens, state, linha)  # passa o número da linha atual

    linha += 1

print(finalizarAssembly(state))  # gera o .data e exibe o assembly completo

print("===== EXECUTAR EXPRESSAO =====")
print(memoria)
print(resultados_py)

exibirResultados(resultados_py)