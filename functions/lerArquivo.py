def ler_arquivo(nomeArquivo):

    try:
        # abre o arquivo em modo leitura
        with open(nomeArquivo, "r") as file:
            linhas = []
            for linha in file:
                linhas.append(linha.rstrip("\n")) # remove o \n do final de cada linha

        return linhas # devolve a lista de linhas
    
    except FileNotFoundError:
        print("Error: O arquivo não existe!") # arquivo não encontrado

    finally:
        try:
            file.close() # garante que o arquivo foi fechado
        except NameError:
            print("Arquivo não foi aberto.") # arquivo nunca chegou a abrir