import csv
from pulp import LpVariable, LpProblem, lpSum, LpMinimize, lpDot

def carregar_matriz_do_csv(caminho_arquivo):
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        leitor_csv = csv.reader(csvfile, delimiter=';')
        nomes_times = next(leitor_csv)[1:]
        matriz = [[int(distancia.split()[0]) for distancia in row[1:]] for row in leitor_csv]

    return nomes_times, matriz

def gerar_tabela_otimizada(nomes_times, matriz_distancia, matriz_partidas):
    # Número de rodadas e times
    num_rodadas = len(matriz_partidas)
    num_times = len(nomes_times)

    # Criar problema de otimização
    prob = LpProblem("Tabela_Otimizada", LpMinimize)

    # Variáveis de decisão: 0 ou 1 (se o time i jogar contra o time j na rodada k)
    x = [[[LpVariable(f"x_{i}_{j}_{k}", 0, 1, LpBinary) for k in range(num_rodadas)] for j in range(num_times)] for i in range(num_times)]

    # Função objetivo: minimizar a soma das distâncias
    prob += lpSum(lpDot(matriz_distancia[i], x[i][j][k]) for i in range(num_times) for j in range(num_times) for k in range(num_rodadas))

    # Restrições: cada time joga exatamente uma vez em cada rodada
    for k in range(num_rodadas):
        for j in range(num_times):
            prob += lpSum(x[i][j][k] for i in range(num_times)) == 1

    # Restrições: cada time joga exatamente uma vez contra cada time i
    for i in range(num_times):
        for j in range(num_times):
            prob += lpSum(x[i][j][k] for k in range(num_rodadas)) == 1

    # Resolvendo o problema
    prob.solve()

    # Extraindo a tabela otimizada
    tabela_otimizada = [[None for _ in range(num_times)] for _ in range(num_rodadas)]
    for k in range(num_rodadas):
        for i in range(num_times):
            for j in range(num_times):
                if x[i][j][k].value() == 1:
                    tabela_otimizada[k][i] = nomes_times[i]
                    tabela_otimizada[k][j] = nomes_times[j]

    return tabela_otimizada

# Carregar matrizes de distância e partidas
nomes_times, matriz_distancia = carregar_matriz_do_csv("./database/matriz-paa.csv")
_, matriz_partidas = carregar_matriz_do_csv("./database/jogos2023.csv")

# Gerar tabela otimizada
nova_tabela = gerar_tabela_otimizada(nomes_times, matriz_distancia, matriz_partidas)

# Imprimir a tabela otimizada
print("Tabela Otimizada:")
for linha in nova_tabela:
    print(linha)
