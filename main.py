'''
Ana Flávia Martins dos Santos (@aflavinhams)
Isabella Vanderlinde Berkembrock (@berkembrockisabella)
Michele Cristina Otta (@micheleotta)
Yejin Chung (@Chungyejin)

Grupo RA1_7
'''
import sys #Usado para acessar sys.argv

#Importar as funções
from functions.lerArquivo import ler_arquivo
from functions.parseExpressao import parseExpressao
from functions.gerarAssembly import gerarAssembly, criarState, finalizarAssembly
from functions.exibirResultados import exibirResultados
from functions.executarExpressao import executarExpressao


#Função principal do programa
def main():
    if len(sys.argv) < 2: #Verifica se o usuário passou o nome do arquivo
        print("Erro caminho do arquivo não especificado") # Se o usuário não passou, retorna a mensagem
        return
    caminho = sys.argv[1]

    arq = ler_arquivo(caminho)

    # Quando o arquivo estiver vazio
    if not arq:
        return

    memoria = {}
    resultados = {}
    linha = 1 
    all_tokens = []

    state = criarState()

    caminho = sys.argv[1] #Guarda o caminho do arquivo
    arq = ler_arquivo(caminho) #Lê o arquivo e retorna uma lista de linhas


    for line in arq:
        line_tokens = parseExpressao(line) #Transforma a linha em tokens
        
        executarExpressao(line_tokens, memoria, resultados, linha) # Executa a expressão e atualiza a memória e o resultado
        gerarAssembly(line_tokens, state, linha)  #Gera código Assemblt pra essa linha

        all_tokens.append(line_tokens) #Guarda os tokens na lista
        
        linha += 1
    
    with open("tokens.txt", "w", encoding="utf-8") as f: # Cria o arquivo tokens.txt
        for linha_tokens in all_tokens: # Escreve os tokens no arquivo
            f.write(str(linha_tokens) + "\n")


    assembly_code = finalizarAssembly(state) # Gera o código Assembly completo

    with open("saida.s", "w", encoding="utf-8") as f: #Salva o código Assembly
        f.write(assembly_code)

    exibirResultados(resultados)


if __name__ == "__main__":
    main()