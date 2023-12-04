import csv
from pulp import LpProblem, LpVariable, lpSum, value

# Função para ler os dados do arquivo CSV
def ler_dados_csv(nome_arquivo):
    with open(nome_arquivo, newline='') as arquivo:
        leitor = csv.reader(arquivo, delimiter=';')
        times = next(leitor)[1:]
        matriz_distancias = [[int(distancia.replace(" Km", "").replace(",", "")) for distancia in linha[1:]] for linha in leitor]
    return times, matriz_distancias

def imprimir_calendario(calendario):
    for i, jogo in enumerate(calendario, start=1):
        print(f"Rodada {i}: {jogo[0]} vs {jogo[1]} - Distância: {jogo[2]} Km")

def imprimir_distancia_percorrida(times_obj):
    for time in times_obj:
        print(f"{time}: Distância Percorrida = {sum(times_obj[time].values())} Km")

def imprimir_metricas(times_obj):
    distancias = [sum(times_obj[time].values()) for time in times_obj]
    media_distancia = sum(distancias) / len(distancias)
    diferenca_distancia = max(distancias) - min(distancias)

    print(f"Média de Distância Percorrida: {media_distancia} Km")
    print(f"Diferença do Maior para o Menor: {diferenca_distancia} Km")

def gerar_calendario_ilp(times, matriz_distancias):
    # Criar problema de programação linear inteira
    prob = LpProblem("Calendario", sense=LpMinimize)

    # Variáveis binárias para indicar se um jogo ocorre
    x = {(i, j): LpVariable(f"x_{i}_{j}", 0, 1, LpInteger) for i in range(len(times)) for j in range(i + 1, len(times))}

    # Função objetivo: minimizar a distância total
    prob += lpSum(matriz_distancias[i][j] * x[i, j] for i in range(len(times)) for j in range(i + 1, len(times))), "Distancia_Total"

    # Restrições para garantir que cada time jogue exatamente uma vez por rodada
    for i in range(len(times)):
        prob += lpSum(x[i, j] + x[j, i] for j in range(i + 1, len(times))) == 1, f"Restricao_unicidade_{i}"

    # Restrições para garantir que cada time jogue contra todos os outros exatamente uma vez
    for j in range(1, len(times)):
        prob += lpSum(x[i, j] + x[j, i] for i in range(j)) == 1, f"Restricao_unicidade_contra_{j}"

    # Resolver o problema
    prob.solve()

    # Extrair o calendário a partir das variáveis
    calendario = []
    for i in range(len(times)):
        for j in range(i + 1, len(times)):
            if value(x[i, j]) == 1:
                distancia_jogo = matriz_distancias[i][j]
                jogo = (times[i], times[j], distancia_jogo)
                calendario.append(jogo)

    return calendario

# Ler dados do arquivo CSV
nome_arquivo_csv = './database/matriz-paa.csv'
times, matriz_distancias = ler_dados_csv(nome_arquivo_csv)

# Gerar calendário usando programação linear inteira
calendario = gerar_calendario_ilp(times, matriz_distancias)

# Verificar se o calendário foi gerado corretamente
if calendario:
    imprimir_calendario(calendario)
    imprimir_distancia_percorrida(times)
    imprimir_metricas(times)
else:
    print("Não foi possível gerar um calendário que atenda às condições.")
