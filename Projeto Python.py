# FUNÇÕES DO PROJETO

# OPERAÇÕES CRUD -> Criar Publicação

import json
def Criar_Publicação(fnome):

    f = open(fnome, 'r', encoding="utf-8") # f é uma lista de dicionários (um dicionário para cada publicação)
    bd = json.load(f)

    abstract = input("Introduza o resumo da publicação: ").strip()
    keywords = input("Introduza palavras-chave da publicação (separadas por vírgula): ").strip()
    doi = input("Introduza o DOI da publicação: ").strip()
    pdf = input("Introduza o pdf da publicação: ").strip()
    publish_date = input("Introduza a data da publicação (A-M-D): ")
    title = input("Introduza o título da publicação: ").strip()
    url = input("Introduza o url da publicação: ").strip()

    authors = [] # lista de dicionários (um dicionário para cada autor)
    mais_autores = True

    while mais_autores:
        name = input("Introduza o nome do autor: ").strip()
        if name == "":
            mais_autores = False
        else:
            affiliation = input(f"Introduza a afiliação de {name}: ").strip()
            authors.append({
                "name": name, 
                "affiliation": affiliation
            })
    
    nova_pub = {
    
    'abstract': abstract,
    'keywords': keywords,
    'authors': authors,
    'doi': doi,
    'pdf': pdf,
    'publish_date': publish_date,
    'title': title,
    'url': url

    }

    if nova_pub != '':
        bd.append(nova_pub)
        f = open(fnome, 'w', encoding="utf-8")
        json.dump(bd, f, ensure_ascii=False, indent=4)
    else:
        return 

# OPERAÇÃO Carregar Base de Dados Para a Memória

import json
def Carregar_BD(fnome):

    f = open(fnome, 'r', encoding='utf-8')
    publicações = json.load(f)
    return publicações

mybd = Carregar_BD('ata_medica_papers.json')

# OPERAÇÃO Distribuição TOP 20 Autores com Mais Publicações

import json
mybd = Carregar_BD('ata_medica_papers.json')

def Distribuição_20A(bd):

    res = {}
    for publicação in bd:
        for author in publicação['authors']:
            nome_autor = author.get('name')
            if nome_autor in res:
                res[nome_autor] = res[nome_autor] + 1
            else:
                res[nome_autor] = 1
    
    top_20 = sorted(res.items(), key=lambda x: x[1], reverse=True)[:20]

    return top_20
