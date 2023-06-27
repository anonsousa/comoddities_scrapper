import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def obter_dados(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
    #Faz a requisição get para a página.
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    #Encontra a tabela com as cotações.
    table = soup.find("table", {"id": "cross_rate_1"})
    
    #Lista para armazenar os dados
    dados = []
    
    for row in table.find_all("tr"):
        #Obtém as table row e table data
        cells = row.find_all("td")
        if len(cells) > 0:
            # Extrai os dados relevantes das células
            metal = cells[1].text.strip()
            mes = cells[2].text.strip()
            ultimo = cells[3].text.strip()
            previo = cells[4].text.strip()
            maxima = cells[5].text.strip()
            minima = cells[6].text.strip()
            var = cells[7].text.strip()
            varp = cells[8].text.strip()
            hora = cells[9].text.strip()
            
            # Adiciona os dados à lista
            dados.append({
                "Metal": metal,
                "Mês": mes,
                "Último": ultimo,
                "Prévio": previo,
                "Máxima": maxima,
                "Mínima": minima,
                "Variação": var,
                "Variação Percentual": varp,
                "Hora": hora
            })
    
    return dados


def salvar_em_excel(dados, nome_arquivo):
    df = pd.DataFrame(dados)
    writer = pd.ExcelWriter(nome_arquivo, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Dados")
    writer.book.close()


# URL do site
url = "https://br.investing.com/commodities/metals"

while True:
# Obtém os dados da página
    dados = obter_dados(url)

# Salva os dados em um arquivo Excel
    nome_arquivo = "metal_data.xlsx"
    salvar_em_excel(dados, nome_arquivo)
    
    # Exibe a mensagem "Dados Atualizados"
    print('\033[94m\033[1mDados Atualizados\033[0m')
    # Aguarda 5 minutos antes de executar novamente
    time.sleep(300)