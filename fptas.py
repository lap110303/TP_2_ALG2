import numpy as np

def mochila_fptas(valores, pesos, capacidade, epsilon=0.1):
    n = len(valores)
    v_max = max(valores)
    mi = epsilon * v_max / n

    valores_escalonados = [int(v // mi) for v in valores]
    V = sum(valores_escalonados)

    dp = [float('inf')] * (V + 1)
    dp[0] = 0

    for i in range(n):
        for v in range(V, valores_escalonados[i] - 1, -1):
            if dp[v - valores_escalonados[i]] + pesos[i] <= capacidade:
                dp[v] = min(dp[v], dp[v - valores_escalonados[i]] + pesos[i])

    for v in range(V, -1, -1):
        if dp[v] <= capacidade:
            return int(v * mi), dp[v]

    return 0, 0
