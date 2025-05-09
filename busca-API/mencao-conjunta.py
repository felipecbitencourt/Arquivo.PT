import requests
from collections import defaultdict
import matplotlib.pyplot as plt

def count_term_correlation(main_term, correlated_term, start_year=2000, end_year=2020):
    correlation_counts = defaultdict(int)
    for year in range(start_year, end_year + 1):
        from_date = f"{year}0101000000"
        to_date = f"{year}1231235959"


        query = f'"{main_term}" AND "{correlated_term}"'

        payload = {
            'q': query,
            'maxItems': 1,
            'from': from_date,
            'to': to_date
        }

        try:
            r = requests.get('https://arquivo.pt/textsearch', params=payload, timeout=10)
            r.raise_for_status()  # Verifica erros HTTP
            data = r.json()
            total_items = data.get('estimated_nr_results', 0)
            correlation_counts[year] = total_items
            print(f"{year}: \"{main_term}\" + \"{correlated_term}\" = {total_items}")
        except Exception as e:
            print(f"Erro em {year}: {str(e)}")
            correlation_counts[year] = 0

    return correlation_counts

# Termos para pesquisa (exemplo com saúde)
termos_pesquisa = [
    "donald trump",
    "jair bolsonaro",
    "Nicolás Maduro",
    "Vladimir Putin",
    "Emmanuel Macron",
    "Marcelo Rebelo de Sousa",
    "Xi Jinping",
    "Kim Jong-un",
    "Benjamin Netanyahu"
]

# Termo principal com aspas inclusas na string
main_term = "fake news" 

# Coletar dados
all_correlation_data = {}
for termo in termos_pesquisa:
    print(f"\nPesquisando: \"{main_term}\" + \"{termo}\"...")
    all_correlation_data[termo] = count_term_correlation(main_term, termo)

# Visualização
plt.figure(figsize=(14, 8))
for termo, data in all_correlation_data.items():
    anos = list(data.keys())
    valores = list(data.values())
    plt.plot(anos, valores, marker='o', label=f'"{termo}"')

plt.title('Menções conjuntas com "fake news" por ano (Arquivo.pt)')
plt.xlabel('Ano')
plt.ylabel('Número de ocorrências')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Legenda fora do gráfico
plt.grid(True, linestyle='--', alpha=0.7)
plt.yscale('log')  # Escala logarítmica para melhor visualização
plt.tight_layout()
plt.show()