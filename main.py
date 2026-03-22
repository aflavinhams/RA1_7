from functions.lerArquivo import ler_arquivo
from functions.parseexpressao import parseExpressao
from functions.gerarAssembly import gerarAssembly


print(f"Arquivo: {ler_arquivo("arquivosTeste/teste.txt")}\n")
arq = ler_arquivo("arquivosTeste/teste.txt")

valid_tokens = []
for line in arq:
    line_tokens = parseExpressao(line)
    print(line_tokens)
    valid_tokens = valid_tokens + parseExpressao(line)


print(gerarAssembly(valid_tokens))