def ler_matriz(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    nomes_times = linhas[0].strip().split(';')[1:]

    matriz = []
    for linha in linhas[1:]:
        valores = linha.strip().split(';')[1:]
        matriz.append([float(valor.split(' ')[0]) if valor != '0 Km' else 0 for valor in valores])

    return nomes_times, matriz


def calcular_distancia(matriz_distancias, nomes_times):
    distancia_total = 0
    info_times = []

    for i in range(len(nomes_times)):
        distancia_time = 0
        oponentes = []

        for j in range(len(nomes_times)):
            if i != j:
                distancia_time += matriz_distancias[i][j]
                oponentes.append({nomes_times[j]: matriz_distancias[i][j]})

        distancia_total += distancia_time
        info_times.append({'time': nomes_times[i], 'distancia_total': distancia_time, 'oponentes': oponentes})

    return {'distancia_total': distancia_total, 'info_times': info_times}

def imprimir_resultados(info_temporada):
    print(f"Distância total percorrida: {info_temporada['distancia_total']} Km")

    for info in info_temporada['info_times']:
        print(f"\nResultados para {info['time']}:")
        print(f"Distância total percorrida: {info['distancia_total']} Km")
        print("Distância para cada time:")

        for oponente in info['oponentes']:
            oponente_nome = list(oponente.keys())[0]
            oponente_distancia = oponente[oponente_nome]
            print(f"{oponente_nome}: {oponente_distancia} Km")

# Chamar as funções
nome_arquivo = 'database/matriz-paa.csv'
nomes_times, matriz_distancias = ler_matriz(nome_arquivo)
distancia_times = calcular_distancia(matriz_distancias, nomes_times)
imprimir_resultados(distancia_times)