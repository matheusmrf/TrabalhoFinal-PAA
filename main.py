def ler_matriz(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    nomes_times = linhas[0].strip().split(';')[1:]

    matriz = []
    for linha in linhas[1:]:
        valores = linha.strip().split(';')[1:]
        matriz.append([float(valor.split(' ')[0]) if valor != '0 Km' else 0 for valor in valores])

    return nomes_times, matriz


def criar_mapeamento_indices(nomes_times):
    return {nome: indice for indice, nome in enumerate(nomes_times)}


def ler_jogos(nome_arquivo, nomes_times_matriz):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    jogos = []
    for linha in linhas[1:]:
        rodada, time_mandante, _, time_visitante = linha.strip().split(';')

        # Adiciona os times ao mapeamento de índices se ainda não estiverem presentes
        if time_mandante not in nomes_times_matriz:
            nomes_times_matriz.append(time_mandante)
        if time_visitante not in nomes_times_matriz:
            nomes_times_matriz.append(time_visitante)

        jogos.append({'rodada': int(rodada), 'time_mandante': time_mandante, 'time_visitante': time_visitante})

    return jogos


def calcular_distancia(matriz_distancias, mapeamento_indices, jogos):
    distancia_total = 0
    info_times = {}

    for jogo in jogos:
        indice_mandante = mapeamento_indices[jogo['time_mandante']]
        indice_visitante = mapeamento_indices[jogo['time_visitante']]

        distancia_time = matriz_distancias[indice_mandante][indice_visitante]
        distancia_total += distancia_time

        # Adiciona informações sobre o jogo para o time mandante
        if jogo['time_mandante'] not in info_times:
            info_times[jogo['time_mandante']] = {'distancia_total': 0, 'oponentes': []}

        info_times[jogo['time_mandante']]['distancia_total'] += distancia_time
        info_times[jogo['time_mandante']]['oponentes'].append({jogo['time_visitante']: distancia_time})

    return {'distancia_total': distancia_total, 'info_times': info_times}


def imprimir_resultados(distancia_times, jogos, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
        arquivo_saida.write(f"Distância total percorrida: {distancia_times['distancia_total']} Km\n")
        arquivo_saida.write("\nResultados por partida:\n")

        for jogo in jogos:
            time_mandante = jogo['time_mandante']
            time_visitante = jogo['time_visitante']

            # Verifica se a chave existe no dicionário antes de acessá-la
            if (
                    time_mandante in distancia_times['info_times']
                    and 'oponentes' in distancia_times['info_times'][time_mandante]
            ):
                oponentes = distancia_times['info_times'][time_mandante]['oponentes']

                # Procura a distância para o time visitante
                distancia_partida = next(
                    (oponente[time_visitante] for oponente in oponentes if time_visitante in oponente),
                    "Informação não disponível",
                )

                arquivo_saida.write(
                    f"\nRodada {jogo['rodada']} - {time_mandante} X {time_visitante} - Distância: {distancia_partida} Km\n")
            else:
                arquivo_saida.write(
                    f"\nRodada {jogo['rodada']} - {time_mandante} X {time_visitante} - Distância: Informação não disponível\n")


# Chamar as funções
nome_arquivo_distancias = './database/matriz-paa.csv'
nome_arquivo_jogos = './database/primeiroTurno2023.csv'
nome_arquivo_saida = './resultados.txt'

nomes_times, matriz_distancias = ler_matriz(nome_arquivo_distancias)
mapeamento_indices = criar_mapeamento_indices(nomes_times)
jogos = ler_jogos(nome_arquivo_jogos, nomes_times)
distancia_times = calcular_distancia(matriz_distancias, mapeamento_indices, jogos)
imprimir_resultados(distancia_times, jogos, nome_arquivo_saida)
