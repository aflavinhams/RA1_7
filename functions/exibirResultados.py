'''
Ana Flávia Martins dos Santos (@aflavinhams)
Isabella Vanderlinde Berkembrock (@berkembrockisabella)
Michele Cristina Otta (@micheleotta)
Yejin Chung (@Chungyejin)

Grupo RA1_7
'''
def exibirResultados(resultados):
    if not resultados: #Se não encontrar os resultados retorna frase que não encontrou
        print("Nenhum resultado encontrado.")
        return

    print("\n===== RESULTADOS =====\n")
    
    for linha in sorted(resultados): #Percorre linha por linha em ordem crescente
        resultado = resultados[linha] #Pega o resultado da expressão da cada linha
        try:
            if float(resultado).is_integer(): #Verifica se o número é inteiro e se for converte o resultado para float
                print(f"[{linha}] -> {int(float(resultado))}") #Se for inteiro converte para int e remove o .0 atrás do número
            else: #Se o número tenha ponto decimais
                print(f"[{linha}] -> {float(resultado):.1f}") #Mostra número com 1 ponto decimal
        except:
            print(f"[{linha}] -> Erro no resultado") #Se acontecer qualquer erro mostra a mensagem de erro ao invés de quebrar o programa
