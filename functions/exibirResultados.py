def exibirResultados(resultados):
    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    print("\n===== RESULTADOS =====\n")

    for i, resultado in enumerate(resultados, start=1):
        try:
            if float(resultado).is_integer():
                print(f"[{i}] -> {int(float(resultado))}")
            else:
                print(f"[{i}] -> {float(resultado):.1f}")
        except:
            print(f"[{i}] -> Erro no resultado")