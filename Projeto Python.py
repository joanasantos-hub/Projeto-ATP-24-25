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

    bd.append(nova_pub)
    f = open(fnome, 'w', encoding="utf-8")
    json.dump(bd, f, ensure_ascii=False, indent=4)


