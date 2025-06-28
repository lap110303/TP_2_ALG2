def mochila_aproximativo_2(valores, pesos, capacidade):
    n = len(valores)
    melhor_unitario = 0
    for i in range(n):
        if pesos[i] <= capacidade:
            melhor_unitario = max(melhor_unitario, valores[i])

    relacoes = [(valores[i] / pesos[i], i) for i in range(n)]
    relacoes.sort(reverse=True)

    peso_total = 0
    valor_total = 0
    for r, i in relacoes:
        if peso_total + pesos[i] <= capacidade:
            peso_total += pesos[i]
            valor_total += valores[i]

    return max(melhor_unitario, valor_total)
