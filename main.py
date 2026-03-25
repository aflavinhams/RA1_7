from functions.lerArquivo import ler_arquivo
from functions.parseexpressao import parseExpressao
from functions.gerarAssembly import gerarAssembly
from functions.exibirResultados import exibirResultados
from functions.executarExpressao import executarExpressao

print(f"Arquivo: {ler_arquivo('arquivosTeste/teste.txt')}\n")
arq = ler_arquivo("arquivosTeste/teste.txt")

valid_tokens = []
resultados = []
memoria = {}
resultados_py = {}
linha = 1

for line in arq:
    line_tokens = parseExpressao(line)
    print(line_tokens)
    executarExpressao(line_tokens, memoria, resultados_py, linha)
    linha += 1

    valid_tokens = valid_tokens + parseExpressao(line)
    resultados.append(len(line_tokens))

print(valid_tokens)
print(gerarAssembly(valid_tokens))

print("===== EXECUTAR EXPRESSAO =====")
print(memoria)
print(resultados_py)

exibirResultados(resultados)