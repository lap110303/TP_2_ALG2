from time import perf_counter
from branch_and_bound import Item, mochila_branch_bound
from fptas import mochila_fptas
from aproximativo_2 import mochila_aproximativo_2
import os

def carregar_instancia(arquivo):
    with open(arquivo) as f:
        n, capacidade = map(float, f.readline().split())
        n = int(n)
        capacidade = float(capacidade)
        valores = []
        pesos = []
        for _ in range(n):
            v, p = map(float, f.readline().split())
            valores.append(v)
            pesos.append(p)
    return valores, pesos, capacidade

def executar_algoritmos(arquivo, epsilon=0.1):
    print(f"\n--- Executando instância: {arquivo} ---")
    valores, pesos, capacidade = carregar_instancia(arquivo)

    itens = [Item(i, valores[i], pesos[i]) for i in range(len(valores))]

    inicio = perf_counter()
    lucro_bnb, itens_bnb = mochila_branch_bound(itens, capacidade)
    tempo_bnb = perf_counter() - inicio
    print(f"Branch-and-Bound: Valor = {lucro_bnb}, Tempo = {tempo_bnb:.6f}s")

    inicio = perf_counter()
    lucro_fptas, _ = mochila_fptas(valores, pesos, capacidade, epsilon)
    tempo_fptas = perf_counter() - inicio
    print(f"FPTAS (ε={epsilon}): Valor = {lucro_fptas}, Tempo = {tempo_fptas:.6f}s")

    inicio = perf_counter()
    lucro_aprox = mochila_aproximativo_2(valores, pesos, capacidade)
    tempo_aprox = perf_counter() - inicio
    print(f"2-aproximativo: Valor = {lucro_aprox}, Tempo = {tempo_aprox:.6f}s")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_instancia> [epsilon]")
        exit(1)
    nome_arquivo = sys.argv[1]
    epsilon = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    executar_algoritmos(nome_arquivo, epsilon)
