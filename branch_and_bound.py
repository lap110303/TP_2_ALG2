import heapq

class Item:
    def __init__(self, indice, valor, peso):
        self.indice = indice
        self.valor = valor
        self.peso = peso
        self.relacao = valor / peso

def mochila_branch_bound(itens, capacidade):
    itens.sort(key=lambda x: x.relacao, reverse=True)
    n = len(itens)

    def limite(nivel, valor, peso):
        if peso > capacidade:
            return 0
        limite_lucro = valor
        peso_total = peso
        i = nivel
        while i < n and peso_total + itens[i].peso <= capacidade:
            peso_total += itens[i].peso
            limite_lucro += itens[i].valor
            i += 1
        if i < n:
            limite_lucro += (capacidade - peso_total) * itens[i].relacao
        return limite_lucro

    No = lambda nivel, valor, peso, limite_superior, selecionados: (
        -limite_superior, nivel, valor, peso, selecionados
    )
    fila = [No(0, 0, 0, limite(0, 0, 0), [])]
    melhor_lucro = 0
    melhor_selecao = []

    while fila:
        _, nivel, valor, peso, selecionados = heapq.heappop(fila)

        if nivel == n:
            if valor > melhor_lucro:
                melhor_lucro = valor
                melhor_selecao = selecionados
            continue

        item = itens[nivel]

        com_item = selecionados + [item.indice]
        valor_com = valor + item.valor
        peso_com = peso + item.peso
        limite_com = limite(nivel + 1, valor_com, peso_com)

        if peso_com <= capacidade and valor_com > melhor_lucro:
            melhor_lucro = valor_com
            melhor_selecao = com_item

        if limite_com > melhor_lucro:
            heapq.heappush(fila, No(nivel + 1, valor_com, peso_com, limite_com, com_item))

        limite_sem = limite(nivel + 1, valor, peso)
        if limite_sem > melhor_lucro:
            heapq.heappush(fila, No(nivel + 1, valor, peso, limite_sem, selecionados))

    return melhor_lucro, melhor_selecao
