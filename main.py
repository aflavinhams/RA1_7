from functions.lerArquivo import ler_arquivo
from functions.parseEspressao import parseExpressao
from functions.gerarAssembly import gerarAssembly
from functions.exibirResultados import exibirResultados  

print(f"Arquivo: {ler_arquivo('arquivosTeste/teste.txt')}\n")
arq = ler_arquivo("arquivosTeste/teste.txt")

valid_tokens = []
resultados = [] 

for line in arq:
    line_tokens = parseExpressao(line)
    print(line_tokens)

    valid_tokens = valid_tokens + parseExpressao(line)
    resultados.append(len(line_tokens))

print(gerarAssembly(valid_tokens))

exibirResultados(resultados)
