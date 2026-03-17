import os
from tqdm import tqdm
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Busca a chave de forma segura
API_KEY = os.getenv('NEXTBILLION_API_KEY')
# Função para calcular distância e tempo usando NextBillion
def calcular_distancia_e_tempo(lat1, lon1, lat2, lon2):
    url = "https://api.nextbillion.io/directions"
    params = {
        'origin': f"{lat1},{lon1}",
        'destination': f"{lat2},{lon2}",
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'routes' in data and len(data['routes']) > 0:
            route = data['routes'][0]

            return route['distance'], route['duration']
    return None, None

# Caminhos de arquivos
caminho_entrada = 'C:/Users/Paulo Fanti/Documents/Arquivos/Romaneios_dezembro_rev.xlsx'
caminho_saida = ('C:/Users/Paulo Fanti/Documents/Arquivos/Results_Romaneios_dezembro_rev.xlsx')

# Carregar planilha
planilha = pd.read_excel(caminho_entrada)
planilha['dh_entrada'] = pd.to_datetime(planilha['dh_entrada'])

# Inicializar colunas novas
planilha['Distancia_Km'] = None
planilha['Tempo_Segundos'] = None
planilha['Distancia_Total_Grupo_Km'] = None
planilha['Tempo_Total_Grupo_S'] = None
planilha['Status_Execucao'] = None

# Agrupar por lista
grupos = list(planilha.sort_values('dh_entrada').groupby('lista_35'))
total_listas = len(grupos)
grupos_com_retorno = []

inicio_tempo = time.time()

for i, (nome_lista, grupo) in enumerate(tqdm(grupos, desc="Processando listas")):
    grupo = grupo.sort_values('dh_entrada').copy()
    indices = grupo.index.tolist()

    distancia_total = 0
    tempo_total = 0

    ponto_anterior = None

    for idx in indices:
        linha = grupo.loc[idx]

        # Ignorar se for uma linha de validação com lat/lon = 0
        if (
            str(linha['origem']).strip().lower() == 'validacao' and
            linha['lat'] == 0 and
            linha['lon'] == 0
        ):
            grupo.at[idx, 'Status_Execucao'] = 'Ignorado_validacao_sem_coords'
            continue

        lat_dest = linha['lat']
        lon_dest = linha['lon']

        if ponto_anterior is not None:
            dist, tempo = calcular_distancia_e_tempo(ponto_anterior[0], ponto_anterior[1], lat_dest, lon_dest)

            if dist is not None and tempo is not None:
                grupo.at[idx, 'Distancia_Km'] = dist / 1000
                grupo.at[idx, 'Tempo_Segundos'] = tempo
                distancia_total += dist / 1000
                tempo_total += tempo
            else:
                grupo.at[idx, 'Distancia_Km'] = 'Erro'
                grupo.at[idx, 'Tempo_Segundos'] = 'Erro'

        ponto_anterior = (lat_dest, lon_dest)

    # Preencher totais
    grupo['Distancia_Total_Grupo_Km'] = round(distancia_total, 3)
    grupo['Tempo_Total_Grupo_S'] = round(tempo_total, 1)
    grupo['Status_Execucao'] = grupo['Status_Execucao'].fillna('Calculado')

    grupos_com_retorno.append(grupo)
    planilha_parcial = pd.concat(grupos_com_retorno, ignore_index=True)
    planilha_parcial.to_excel(caminho_saida, index=False)

    # Progresso
    porcentagem = (i + 1) / total_listas * 100
    tempo_passado = time.time() - inicio_tempo
    tempo_medio = tempo_passado / (i + 1)
    restante = (total_listas - (i + 1)) * tempo_medio
    minutos, segundos = divmod(int(restante), 60)
    print(f" Lista {nome_lista} salva. Progresso: {porcentagem:.1f}% | Restante: {minutos}m{segundos}s")

print(f"\n Processamento finalizado. Arquivo salvo em:\n{caminho_saida}")
