def ler_arquivo(nomeArquivo):

    try:

        with open(nomeArquivo, "r") as file:
            linhas = []
            for linha in file:
                linhas.append(linha)

        return linhas
    
    except FileNotFoundError:
        print("Error: O arquivo não existe!")


    finally:
        try:
            file.close()
        except NameError:
            print("Arquivo não foi aberto.")

print(ler_arquivo("arquivosTeste/teste.txt"))