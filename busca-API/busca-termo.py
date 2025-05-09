import requests
import datetime
import matplotlib.pyplot as plt

# Parâmetros
query = '"fake news"'
anos = list(range(2000, 2021))  # ajustável
resultados_por_ano = []

for ano in anos:
    from_date = int(f"{ano}0101000000")
    to_date = int(f"{ano}1231235959")

    payload = {'q': query, 'from': from_date, 'to': to_date, 'maxItems': 1}
    print(payload)
    r = requests.get('http://arquivo.pt/textsearch', params=payload)
    data = r.json()

    estimado = int(data.get("estimated_nr_results", 0))
    resultados_por_ano.append(estimado)
    print(f"{ano}: {estimado} ocorrências")

# Soma total de ocorrências
total = sum(resultados_por_ano)
print(f"\nTotal de ocorrências de '{query}' entre {anos[0]} e {anos[-1]}: {total}")

# Gráfico
plt.figure(figsize=(12,6))
plt.plot(anos, resultados_por_ano, marker='o', color='purple')
plt.yscale('log') 

plt.title(f'Menções no título ao termo {query} por ano em jornais selecionados (Arquivo.pt)')
plt.xlabel('Ano')
plt.ylabel('Número estimado de ocorrências (escala log)')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
