# FUNÇÕES DO PROJETO

# OPERAÇÕES CRUD -> Criar Publicação

import json
def Criar_Publicação(fnome):

    with open(fnome, 'r', encoding='utf-8') as f: # f é uma lista de dicionários (um dicionário para cada publicação)
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
            orcid =  input(f"Introduza o orcid de {name}").strip()
            authors.append({
                "name": name, 
                "affiliation": affiliation,
                "orcid": orcid
            })
            
    for author in authors:
        if author.get('affiliation') == '':
            del author['affiliation']
        if author.get('orcid') == '':
            del author['orcid']
    
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

    nova_pub = {chave: valor for chave,valor in nova_pub.items() if valor} # Garante que se uma chave não possuir informação não será criada essa entrada no dicionário da nova publicação

    if nova_pub.get('title'): # Garante que existe um título para a publicação (requisito obrigatório)
        bd.append(nova_pub)
        with open(fnome, 'w', encoding='utf-8') as f:
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

# Consultar pub por título e listar informação organizada

def Consultar_Publicacao(mybd):
    busca = input("Digite o título da publicação: ").strip()
    for pub in mybd:
        if pub.get('title') and pub['title'].lower() == busca.lower():
            print("\n=== Detalhes da Publicação ===")
            print(f"Título: {pub['title']}")
            print(f"Resumo: {pub['abstract']}")
            print(f"Palavras-chave: {pub['keywords']}")
            print(f"DOI: {pub['doi']}")
            print(f"PDF: {pub['pdf']}")
            print(f"Data de Publicação: {pub['publish_date']}")
            print(f"URL: {pub['url']}")
            print("\n--- Autores ---")
            for autor in pub['authors']:
                print(f"Nome: {autor.get('name', 'Nome não disponível')}, "
                          f"Afiliação: {autor.get('affiliation', 'Afiliação não disponível')}, "
                          f"ORCID: {autor.get('orcid', 'ORCID não disponível')}")
            return
    return (f"Nenhuma publicação encontrada com o título: '{busca}'")


mybd = Carregar_BD('ata_medica_papers.JSON')
Consultar_Publicacao(mybd)

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

    return dict(top_20)

# OPERAÇÃO Distribuição de Publicações Por Ano

import json
mybd =  Carregar_BD('ata_medica_papers.json')

def Distribuição_Ano(bd):

    res = {}
    for publicação in bd:
        data_pub = publicação.get('publish_date')
        if data_pub: # Garante que existe essa entrada no dicionário
            ano = data_pub.split('-')[0]
            if ano in res:
                res[ano] = res[ano] + 1
            else:
                res[ano] = 1
    return dict(sorted(res.items()))
    
# OPERAÇÃO Distribuição Publicações Por Mês em x Ano

import json
mybd = Carregar_BD('ata_medica_papers.json')

def Distribuição_Mês(bd):

    x = input('Introduza o ano que pretende analisar: ') # x é o input do ano que queremos analisar
    res = {}
    for publicação in bd:
        data_pub = publicação.get('publish_date')
        if data_pub: # Garante que existe essa entrada no dicionário
            ano = data_pub.split('-')[0]
            mês = data_pub.split('-')[1]
            if x == ano:
                if mês in res:
                    res[mês] = res[mês] + 1
                else:
                    res[mês] = 1
    return dict(sorted(res.items()))

# OPERAÇÃO Distribuição TOP 20 Palavras-Chave Mais Frequentes

import json
mybd =  Carregar_BD('ata_medica_papers.json')

def Distribuição_20PC(bd):

    res = {}
    for publicações in bd:
        palavras_chaves = publicações.get('keywords')
        if palavras_chaves: # Garante que existe essa entrada no dicionário
            lista_palavras = palavras_chaves.split(',') # Criamos uma lista com as palavras-chave de cada publicação
            for pc in lista_palavras:
                pc = pc.strip(' .')
                if pc in res:
                    res[pc] = res[pc] + 1
                else:
                    res[pc] = 1

    top_20 = sorted(res.items(), key=lambda x: x[1], reverse=True)[:20]

    return dict(top_20)

# OPERAÇÃO Distribuição Publicações de x Autor Por Ano

import json
mybd = Carregar_BD('ata_medica_papers.json')

def Distribuição_Autor(bd):

    nome = input('Introduza o nome do autor: ').strip().lower()
    res = {}
    for publicação in bd:
        data_pub = publicação.get('publish_date')
        if data_pub: # Garante que existe essa entrada no dicionário
            for author in publicação.get('authors'):
                nome_autor = author.get('name').strip().lower()
                if nome == nome_autor:
                    ano = data_pub.split('-')[0]
                    if ano in res:
                        res[ano] = res[ano] + 1
                    else:
                        res[ano] = 1
    return dict(sorted(res.items()))

# OPERAÇÃO Distribuição Palavra-Chave Mais Frequente Por Ano (TOP 1)

import json
mybd = Carregar_BD('ata_medica_papers.json')

def Distribuição_PC(bd):

    res = {}
    for publicações in bd:
        data_pub = publicações.get('publish_date')
        palavras_chaves = publicações.get('keywords')
        if data_pub and palavras_chaves: # Garante que existem essas entradas no dicionário
            ano = data_pub.split('-')[0]
            lista_palavras = palavras_chaves.split(',')
            if ano not in res:
                res[ano] = {}
            for pc in lista_palavras:
                pc = pc.strip(' .')
                if pc in res[ano]:
                    res[ano][pc] = res[ano][pc] + 1
                else:
                    res[ano][pc] = 1

    # res é finalizado como um dicionário em que as chaves são os anos e os valores serão dicionários com a contagem das palavras-chave

    pc_mais_frequente = {}
    for ano, pc in res.items():
        top_1 = sorted(pc.items(), key=lambda x: x[1], reverse=True)[:1]
        if top_1:  # Garante que existe pelo menos uma palavra-chave no TOP 1
            pc_mais_frequente[ano] = top_1[0]

    # O método pc.items() vai transformar os dicionários com a contagem de palavras-chave numa lista de tuplos que será sorted de modo a retornar apenas a palavra-chave mais frequente para cada ano   

    return pc_mais_frequente

# OPERAÇÃO Listar Autores no Ficheiro de Suporte

import json
mybd = Carregar_BD('ata_medica_papers.json')

def Listar_Autores(bd):
    print('---- Lista de Autores ----\n')
    for publicações in bd:
        for author in publicações.get('authors'):
            print(f'Autor: {author.get('name')}\nPublicação: {publicações.get('title')}\n')

# OPERAÇÃO Listar Publicações com x Palavras-Chave do Ficheiro de Suporte

import json
mybd = Carregar_BD('ata_medica_papers.json')

def Listar_Pub_PC(bd):

    palavra_chave = input('Introduza a palavra-chave que deseja procurar: ')
    print('---- Lista de Publicações ----\n')
    for publicação in bd:
        if publicação.get('keywords'):
            if palavra_chave in publicação.get('keywords'):
                print(f'Publicação: {publicação.get('title')}\nPalavras-Chave: {publicação.get('keywords')}\n')

# OPERAÇÃO Importar Publicações de Ficheiro Externo JSON

import json

def Importar_Pub(fnome):

    with open(fnome, 'r', encoding='utf-8') as f: # Lemos o ficheiro externo
        novos_registos = json.load(f)

    with open('ata_medica_papers.json', 'r', encoding='utf-8') as f2: # Lemos o ficheiro principal com a nossa bd
        bd = json.load(f2)

    for registos in novos_registos:
            if registos.get('title'): # Os registos válidos no ficheiro externo serão adicionados à bd
                bd.append(registos)

    with open('ata_medica_papers.json', 'w', encoding='utf-8') as f2: #Abrimos o ficheiro principal para escrita e implementamos a nova bd atualizada com os novos registos
        json.dump(bd, f2, ensure_ascii=False, indent=4)
