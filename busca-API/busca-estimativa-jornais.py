import requests

# Parâmetros
site = "https://www.cmjornal.pt/"  # Domínio do jornal
payload = {
    'q': '*',             # Busca por qualquer termo
    'siteSearch': site,   # Filtra apenas pelo domínio
    'maxItems': 1         # Só precisamos do total estimado
}

response = requests.get('http://arquivo.pt/textsearch', params=payload)
data = response.json()

total_arquivado = data.get("estimated_nr_results", "Indisponível")
print(f"Total de páginas do {site} no Arquivo.pt: {total_arquivado}")