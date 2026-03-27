import sys

from functions.lerArquivo import ler_arquivo
from functions.parseexpressao import parseExpressao
from functions.gerarAssembly import gerarAssembly, criarState, finalizarAssembly
from functions.exibirResultados import exibirResultados
from functions.executarExpressao import executarExpressao

def main():
    if len(sys.argv) < 2:
        print("Erro caminho do arquivo não especificado")
        return

    caminho = sys.argv[1]

    print(f"Arquivo: {caminho}\n")
    arq = ler_arquivo(caminho)

    memoria = {}
    resultados = {}
    linha = 1
    all_tokens = []

    state = criarState()  # cria o estado compartilhado entre todas as linhas

    for line in arq:
        line_tokens = parseExpressao(line)
        all_tokens.append(line_tokens)
        
        executarExpressao(line_tokens, memoria, resultados, linha)
        gerarAssembly(line_tokens, state, linha)  # passa o número da linha atual

        all_tokens.append(line_tokens)
        
        linha += 1
    
    with open("tokens.txt", "w", encoding="utf-8") as f:
        for linha_tokens in all_tokens:
            f.write(str(linha_tokens) + "\n")


    assembly_code = finalizarAssembly(state)

    with open("saida.asm", "w", encoding="utf-8") as f:
        f.write(assembly_code)

    print("===== EXECUTAR EXPRESSÃO =====\n")
    print(memoria)
    print(resultados)


    exibirResultados(resultados)
    

if __name__ == "__main__":
    main()