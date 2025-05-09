import requests
import matplotlib.pyplot as plt
from collections import defaultdict

# Configurações
query = '"fake news"'  
anos = list(range(2000, 2021))  

# Lista de veículos de notícias
veiculos = {
    "Público": "https://www.publico.pt/",
    "Diário de Notícias": "https://www.dn.pt/",
    "SIC Notícias": "https://sicnoticias.pt/",
    "RTP": "https://www.rtp.pt/",
    "Observador": "https://observador.pt/",
    "Correio da Manhã": "https://www.cmjornal.pt/"
}

# Dicionário para armazenar resultados
resultados = defaultdict(dict)

# Função para buscar dados
def buscar_ocorrencias(veiculo, site):
    print(f"\nBuscando no {veiculo}...")
    for ano in anos:
        try:
            payload = {
                'q': query,
                'siteSearch': site,
                'from': f"{ano}0101000000",
                'to': f"{ano}1231235959",
                'maxItems': 1
            }
            response = requests.get('https://arquivo.pt/textsearch', params=payload, timeout=15)
            data = response.json()
            resultados[veiculo][ano] = data.get("estimated_nr_results", 0)
            print(f"{ano}: {resultados[veiculo][ano]} ocorrências")
        except Exception as e:
            print(f"Erro em {ano}: {e}")
            resultados[veiculo][ano] = 0

# Executa as buscas para todos os veículos
for veiculo, site in veiculos.items():
    buscar_ocorrencias(veiculo, site)

# Configuração do gráfico
plt.figure(figsize=(14, 8))
cores = ['#FF4040', '#1E90FF', '#32CD32', '#FF8C00', '#9370DB', '#FF1493']

# Plotagem para cada veículo
for idx, (veiculo, dados) in enumerate(resultados.items()):
    anos_ordenados = sorted(dados.keys())
    valores = [dados[ano] for ano in anos_ordenados]
    plt.plot(anos_ordenados, valores,
             marker='o',
             linestyle='-',
             linewidth=2,
             markersize=6,
             color=cores[idx % len(cores)],
             label=veiculo)

# Customização do gráfico
plt.title(f'Menções a {query} em Diferentes Veículos (2000-2023)', fontsize=16, pad=20)
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Ocorrências estimadas', fontsize=12)
plt.yscale('log')  # Escala logarítmica
plt.grid(True, which="both", linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Adiciona anotações para o pico de cada veículo
for veiculo, dados in resultados.items():
    max_ano = max(dados, key=dados.get)
    max_valor = dados[max_ano]
    if max_valor > 0:
        plt.annotate(f'{veiculo[:3]}: {max_valor}',
                    xy=(max_ano, max_valor),
                    xytext=(max_ano, max_valor*1.5),
                    arrowprops=dict(facecolor='black', arrowstyle='->'),
                    fontsize=9)

plt.show()