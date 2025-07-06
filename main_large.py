from time import perf_counter
import tracemalloc
import csv
import sys
from branch_and_bound import Item, mochila_branch_bound
from fptas import mochila_fptas
from aproximativo_2 import mochila_aproximativo_2

def carregar_info(arquivo_info):
    n = None
    capacidade = None
    with open(arquivo_info, newline='') as f:
        leitor = csv.reader(f)
        for linha in leitor:
            if not linha:
                continue
            chave = linha[0].strip().lower()
            valor = linha[1].strip()
            if chave == 'n':
                n = int(valor)
            elif chave == 'c':
                capacidade = float(valor)
    if n is None or capacidade is None:
        raise ValueError("Arquivo info.csv não contém 'n' ou 'c'")
    return n, capacidade

def carregar_itens(arquivo_itens, n_esperado=None):
    valores = []
    pesos = []
    with open(arquivo_itens, newline='') as f:
        leitor = csv.DictReader(f)
        leitor.fieldnames = [nome.strip() for nome in leitor.fieldnames]
        for linha in leitor:
            linha = {k.strip(): v for k, v in linha.items()}
            valores.append(float(linha['price']))
            pesos.append(float(linha['weight']))
    if n_esperado is not None and len(valores) != n_esperado:
        raise ValueError(f"Quantidade de itens ({len(valores)}) não bate com n={n_esperado}")
    return valores, pesos

def executar_algoritmos_csv(arquivo_itens, arquivo_info, epsilon=0.1):
    print(f"\n--- Executando instância grande CSV: {arquivo_itens} + {arquivo_info} ---")
    n, capacidade = carregar_info(arquivo_info)
    valores, pesos = carregar_itens(arquivo_itens, n_esperado=n)
    itens = [Item(i, valores[i], pesos[i]) for i in range(len(valores))]

    # Branch-and-Bound
    tracemalloc.start()
    inicio = perf_counter()
    lucro_bnb, _ = mochila_branch_bound(itens, capacidade)
    tempo_bnb = perf_counter() - inicio
    pico_bnb = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"Branch-and-Bound: Valor = {lucro_bnb}, Tempo = {tempo_bnb:.6f}s, Memória = {pico_bnb:.2f} KB")

    # FPTAS
    tracemalloc.start()
    inicio = perf_counter()
    lucro_fptas, _ = mochila_fptas(valores, pesos, capacidade, epsilon)
    tempo_fptas = perf_counter() - inicio
    pico_fptas = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"FPTAS (ε={epsilon}): Valor = {lucro_fptas}, Tempo = {tempo_fptas:.6f}s, Memória = {pico_fptas:.2f} KB")

    # 2-aproximativo
    tracemalloc.start()
    inicio = perf_counter()
    lucro_aprox = mochila_aproximativo_2(valores, pesos, capacidade)
    tempo_aprox = perf_counter() - inicio
    pico_aprox = tracemalloc.get_traced_memory()[1] / 1024
    tracemalloc.stop()
    print(f"2-aproximativo: Valor = {lucro_aprox}, Tempo = {tempo_aprox:.6f}s, Memória = {pico_aprox:.2f} KB")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python main_large.py <arquivo_items.csv> <arquivo_info.csv> [epsilon]")
        exit(1)
    arquivo_itens = sys.argv[1]
    arquivo_info = sys.argv[2]
    epsilon = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    executar_algoritmos_csv(arquivo_itens, arquivo_info, epsilon)
