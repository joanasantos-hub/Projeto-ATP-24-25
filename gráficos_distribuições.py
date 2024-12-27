# GRÁFICOS DE DISTRIBUIÇÕES

import json
import matplotlib.pyplot as plt
from funções_principais import Carregar_BD, Distribuição_20A, Distribuição_20PC, Distribuição_PC, Distribuição_Ano, Distribuição_Mês, Distribuição_Autor


mybd = Carregar_BD('ata_medica_papers.json')


# Distribuição TOP 20 AUTORES
dist_20A = Distribuição_20A(mybd)

plt.figure(figsize=(10, 6))
plt.bar(dist_20A.keys(), dist_20A.values(), color= 'hotpink')
plt.title('Top 20 Autores com Mais Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xlabel('Autores', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xticks(rotation=45, ha='right', fontname='Arial Rounded Mt Bold')
plt.tight_layout()
plt.show()

# Distribuição TOP 20 PALAVRAS-CHAVE
dist_20PC = Distribuição_20PC(mybd)

plt.figure(figsize=(10, 6))
plt.bar(dist_20PC.keys(), dist_20PC.values(), color= 'hotpink')
plt.title('Top 20 Palavras-Chave Mais Frequentes', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xlabel('Palavras-Chave', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.ylabel('Frequência', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
plt.tight_layout()
plt.show()

# Distribuição TOP 1 PALAVRAS-CHAVE POR ANO
dist_PC = Distribuição_PC(mybd)

anos = list(dist_PC.keys()) # Lista de anos
palavras = [item[0] for item in dist_PC.values()] # Lista de palavras-chave
contagens = [item[1] for item in dist_PC.values()] # Lista de contagens de cada palavra

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
plt.show()

# Distribuição PUBLICAÇÕES POR ANO
dist_Ano = Distribuição_Ano(mybd)

plt.figure(figsize=(10, 6))
plt.bar(dist_Ano.keys(), dist_Ano.values(), color= 'hotpink')
plt.title('Publicações Por Ano', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xlabel('Anos', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
plt.tight_layout()
plt.show()

# Distribuição PUBLICAÇÕES POR MÊS NUM ANO
dist_Mês = Distribuição_Mês(mybd)

plt.figure(figsize=(10, 6))
plt.bar(dist_Mês.keys(), dist_Mês.values(), color= 'hotpink')
plt.title('Publicações Por Mês', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xlabel('Meses', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
plt.tight_layout()
plt.show()

# Distribuição PUBLICAÇÕES DE UM AUTOR POR ANO -> ATENÇÃO alguns números não irão bater certo devido à presença de publicações sem data
dist_Autor = Distribuição_Autor(mybd)

plt.figure(figsize=(10, 6))
plt.bar(dist_Autor.keys(), dist_Autor.values(), color= 'hotpink')
plt.title('Publicações Por Ano', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xlabel('Anos', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.ylabel('Número de Publicações', fontdict={'fontname': 'Arial Rounded Mt Bold'})
plt.xticks(rotation= 45, ha='right', fontname='Arial Rounded Mt Bold')
plt.tight_layout()
plt.show()