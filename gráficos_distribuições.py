# GRÁFICOS DE DISTRIBUIÇÕES

import json
import matplotlib.pyplot as plt
from interface_linhacmd import Carregar_BD

mybd = Carregar_BD('ata_medica_papers.json')

# Distribuição TOP 20 AUTORES
def graf_20A(dist):
    plt.figure(figsize=(10, 6))
    plt.bar(dist.keys(), dist.values(), color= 'hotpink')
    plt.title('Top 20 Autores com Mais Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xlabel('Autores', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xticks(rotation=45, ha='right', fontname='Arial Rounded Mt Bold')
    plt.tight_layout()
    plt.show(block= False)

# Distribuição TOP 20 PALAVRAS-CHAVE
def graf_20PC(dist):
    plt.figure(figsize=(10, 6))
    plt.bar(dist.keys(), dist.values(), color= 'hotpink')
    plt.title('Top 20 Palavras-Chave Mais Frequentes', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xlabel('Palavras-Chave', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.ylabel('Frequência', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
    plt.tight_layout()
    plt.show(block= False)

# Distribuição TOP 1 PALAVRAS-CHAVE POR ANO
def graf_PC(dist):

    anos = list(dist.keys()) # Lista de anos
    palavras = [item[0] for item in dist.values()] # Lista de palavras-chave
    contagens = [item[1] for item in dist.values()] # Lista de contagens de cada palavra

    plt.figure(figsize=(10,6))
    plt.bar(anos, contagens, color= 'hotpink')
    plt.title('Palavra-Chave Mais Frequente Por Ano', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xlabel('Anos', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.ylabel('Frequência', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')

    for i, (ano, palavra, contagem) in enumerate(zip(anos, palavras, contagens)):
        plt.text(i, contagem + 0.5, palavra, ha= 'center', fontsize=10, fontname='Arial Rounded Mt Bold')
    # Utilizamos o zip() para combinar as 3 listas (anos, palavras e contagens) numa única lista de tuplos -> Cada elemento do tuplo é dado pelos elementos das 3 listas com o devido índice

    plt.tight_layout()
    plt.show(block= False)

# Distribuição PUBLICAÇÕES POR ANO
def graf_Ano(dist):
    plt.figure(figsize=(10, 6))
    plt.bar(dist.keys(), dist.values(), color= 'hotpink')
    plt.title('Publicações Por Ano', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xlabel('Anos', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
    plt.tight_layout()
    plt.show(block= False)

# Distribuição PUBLICAÇÕES POR MÊS NUM ANO
def graf_Mês(dist):
    plt.figure(figsize=(10, 6))
    plt.bar(dist.keys(), dist.values(), color= 'hotpink')
    plt.title('Publicações Por Mês', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xlabel('Meses', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
    plt.tight_layout()
    plt.show(block= False)

# Distribuição PUBLICAÇÕES DE UM AUTOR POR ANO -> ATENÇÃO alguns números não irão bater certo devido à presença de publicações sem data
def graf_Autor(dist):
    plt.figure(figsize=(10, 6))
    plt.bar(dist.keys(), dist.values(), color= 'hotpink')
    plt.title('Publicações Por Ano', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xlabel('Anos', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
    plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
    plt.tight_layout()
    plt.show(block= False)
