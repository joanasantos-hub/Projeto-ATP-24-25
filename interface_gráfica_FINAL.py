import PySimpleGUI as sg
import json
from datetime import datetime
from collections import Counter
from collections import defaultdict
from multiprocessing import Process
import interface_linhacmd as logic
import gráficos_distribuições as gd

sg.theme('LightPurple')

publicações = logic.mybd  # Lista das publicações na base de dados

# ------------- INTERFACE GRÁFICA -------------

def hoje():
    # Retorna a data atual
    return datetime.today().date()

def criar_layout(publicações): 

    menu_botoes = [

        [
        sg.Button("Criar Publicação", key= "-CRIAR-"),
        sg.Button("Atualizar Publicação", key= "-ATUALIZAR-"),
        sg.Button("Apagar Publicação", key= "-APAGAR-"),
        sg.Button("Recuperar Publicações Apagadas", key= "-RECUPERAR-")
    ],
    [
        sg.Button("Consultar Por Título", key= "-CONSULTAR_POR_TITLE-"),
        sg.Button("Consultar Por PDF", key= "-CONSULTAR_POR_PDF-"),
        sg.Button("Consultar Por DOI", key= "-CONSULTAR_POR_DOI-"),
        sg.Button("Consultar Por URL", key= "-CONSULTAR_POR_URL-")
    ],
    [
        sg.Button("Listar Autores", key= "-LISTAR_AUTORES-"),
        sg.Button("Listar Publicações Por Autor", key= "-LISTAR_PUB_AUTOR-"),
        sg.Button("Listar Publicações Por Afiliação", key= "-LISTAR_PUB_AFIL-"),
        sg.Button("Listar Publicações Por Data", key= "-LISTAR_DATA_PUB-")
    ],
    [
        sg.Button("Listar Publicações Por Palavra-Chave", key= "-LISTAR_PUB_PC-"),
        sg.Button("Gerar Relatórios", key= "-RELATORIOS-"),
        sg.Button("Gerar Gráficos", key= "-GRAFICOS-"),
        sg.Button("Importar Publicações", key= "-IMPORTAR-")
    ]
    ]

    layout = [
        [sg.Column(menu_botoes)]
    ]
    return layout

# Layout Para Criar Nova Publicação
def Criar_Pub_Layout():
    
    layout = [
        [sg.Text("Título:", key= '-TEXTO_TITLE-'), sg.Input(key="-TITULO-")],
        [sg.Text("Palavras-chave:", key= '-TEXTO_PC-'), sg.Input(key="-KEYWORDS-")],
        [sg.Text("Resumo:", key= '-TEXTO_ABSTRACT-'), sg.Multiline(size=(50, 5), key="-ABSTRACT-")],
        [sg.Text("Data de Publicação (A-M-D):", key= '-TEXTO_DATA-'), sg.Input(key="-DATA-")],
        [sg.Text("DOI:", key= '-TEXTO_DOI-'), sg.Input(key="-DOI-")],
        [sg.Text("PDF:", key= '-TEXTO_PDF-'), sg.Input(key="-PDF-")],
        [sg.Text("URL:", key= '-TEXTO_URL-'), sg.Input(key="-URL-")],
        [sg.Text("Autores (Nome, Afiliação, ORCID separados por vírgula):", key= '-TEXTO_AUTORES-')],
        [sg.Multiline(size=(50, 5), key="-AUTORES-")],
        [sg.Button("Salvar", key="-SALVAR_PUBLICACAO-"), sg.Button("Cancelar", key="-CANCELAR_PUBLICACAO-")]
    ]

    # Processamento de Informação da Nova Publicação
    def Salvar_Pub(values, publicações):
    
        autores = []
        autores_input = values["-AUTORES-"].strip()

        if autores_input:
            for linha in autores_input.split("\n"):
                campos = [c.strip() for c in linha.split(",")]

                if len(campos) >= 1:
                    autor = {"name": campos[0]}
                    if len(campos) > 1 and campos[1]:
                        autor["affiliation"] = campos[1]
                    elif len(campos) > 2 and campos[2]:
                        autor["orcid"] = campos[2]
                    autores.append(autor)

        dados_publicação = {

            "title": values["-TITULO-"].strip(),
            "keywords": values["-KEYWORDS-"].strip(),
            "abstract": values["-ABSTRACT-"].strip(),
            "publish_date": values["-DATA-"].strip(),
            "doi": values["-DOI-"].strip(),
            "pdf": values["-PDF-"].strip(),
            "url": values["-URL-"].strip(),
            "authors": autores
        
        }

        return dados_publicação

    window = sg.Window('Criar Nova Publicação', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
                window.close()
                return

        elif event == "-SALVAR_PUBLICACAO-":

            dados_publicação = Salvar_Pub(values, publicações)
            logic.Criar_Pub(
                publicações,
                title = dados_publicação["title"],
                keywords = dados_publicação["keywords"],
                abstract = dados_publicação["abstract"],
                publish_date = dados_publicação["publish_date"],
                doi = dados_publicação["doi"],
                pdf = dados_publicação["pdf"],
                url = dados_publicação["url"],
                authors = dados_publicação["authors"]
            )
            
            sg.popup("Publicação criada com sucesso!")
        
        elif event == '-CANCELAR_PUBLICACAO-':
            window.close()

def Apagar_Pub_Layout_():

    layout = [[sg.Text('Introduza o título da publicação que deseja apagar da base de dados:', key= '-TEXTO-')],
        [sg.Text("Título:", key= '-APAGAR_TITLE-'), sg.Input(key="-APAGAR_TITULO-")],
        [sg.Button("Procurar", key="-PROCURAR_APAGAR-"), sg.Button("Cancelar", key="-CANCELAR_APAGAR-")]
    ]
    
    window = sg.Window('Apagar Publicação', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
                window.close()
                return
        
        elif event == "-PROCURAR_APAGAR-":
    
            apagar_title = values["-APAGAR_TITULO-"].strip(' .').lower()

            if apagar_title:
                remover_pubs = [pub for pub in publicações if pub.get('title','').strip(' .').lower() == apagar_title]
                if remover_pubs:
                    logic.Apagar_Pub(publicações, apagar_title)
                    sg.popup(f'A publicação "{apagar_title}" foi apagada com sucesso!')
                else:
                    sg.popup(f'Nenhuma publicação encontrada com o título "{apagar_title}".')
            else:
                sg.popup("Por favor, insira um título válido.")
        
        elif event == '-CANCELAR_APAGAR-':
            window.close()

def Atualizar_Pub_Layout():

    layout = [[sg.Text('Introduza o título da publicação que deseja atualizar:', key= '-TEXTO-')],
        [sg.Text("Título:", key= "-ATUALIZAR_TITLE-"), sg.Input(key= "-ATUALIZAR_TITULO-")],
        [sg.Button("Procurar", key= "-PROCURAR_ATUALIZAR-"), sg.Button("Cancelar", key= "-CANCELAR_PROCURAR-")]
    ]
    
    window = sg.Window('Atualizar Publicação', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return

        elif event == '-PROCURAR_ATUALIZAR-':

            busca_title = values["-ATUALIZAR_TITULO-"].strip()
            
            if busca_title:
               
                publicação = logic.Atualizar_Pub(publicações, busca_title,'','','') # Durante a procura da publicação a atualizar não definimos já o resto dos argumentos
               
                if publicação:
                   
                    detalhes = ["\n=== Detalhes da Publicação ==="]
                    if publicação.get('title'):
                        detalhes.append(f"Título: {publicação['title']}")
                    elif publicação.get('abstract'):
                        detalhes.append(f"Resumo: {publicação['abstract']}")
                    elif publicação.get('keywords'):
                        detalhes.append(f"Palavras-chave: {publicação['keywords']}")
                    elif publicação.get('doi'):
                        detalhes.append(f"DOI: {publicação['doi']}")
                    elif publicação.get('pdf'):
                        detalhes.append(f"PDF: {publicação['pdf']}")
                    elif publicação.get('publish_date'):
                        detalhes.append(f"Data de Publicação: {publicação['publish_date']}")
                    elif publicação.get('url'):
                        detalhes.append(f"URL: {publicação['url']}")
                    
                    detalhes.append("\n--- Autores ---")
                    for autor in publicação.get('authors', []):
                        detalhes.append(
                            f"name: {autor.get('name', 'Nome não disponível')} ::: "
                            f"affiliation: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                            f"orcid: {autor.get('orcid', 'ORCID não disponível')}")

                    detalhes_texto = "\n".join(detalhes) # Juntamos as informações todas dentro da lista de detalhes numa só string

                    window.extend_layout(window, [
                        [sg.Multiline(detalhes_texto, size=(60, 15), disabled=True, key="-DETALHES_PUBLICACAO-")],
                        [sg.Text("Campo a alterar:", size=(30, 1), key='-TEXTO_CAMPO-'), sg.Input(key="-ALTERAR_CHAVE-")],
                        [sg.Text("Informação do campo atualizada:", size=(30, 1), key='-TEXTO_INFO-'), sg.Input(key="-UPDATE_CHAVE-")],
                        [sg.Text("Informação do autor atualizada (se aplicável):", size=(35, 1), key='-TEXTO_AUTOR-'), sg.Input(key="-UPDATE_AUTOR-")],
                        [sg.Button("Salvar Alterações", key="-SALVAR_ATUALIZACAO-"), sg.Button("Cancelar Atualização", key="-CANCELAR_ATUALIZACAO-")]
                    ])
                   
                else:
                    sg.popup(f'Nenhuma publicação encontrada com o título "{busca_title}".')
            else:
                sg.popup("Por favor, insira um título válido.")

        elif event == '-CANCELAR_PROCURAR-':
            window.close()

        elif event == "-SALVAR_ATUALIZACAO-":

            alterar_chave = values["-ALTERAR_CHAVE-"].strip()
            update_chave = values["-UPDATE_CHAVE-"].strip()
            update_autor = values["-UPDATE_AUTOR-"].strip()

            if alterar_chave and (update_chave or update_autor):
                logic.Atualizar_Pub(publicações, busca_title, alterar_chave, update_chave, update_autor)
                sg.popup("Publicação atualizada com sucesso!")

            else:
                sg.popup("Por favor, preencha os campos corretamente.")

        elif event == '-CANCELAR_ATUALIZACAO-':
            window.close()

def Consultar_Title_Layout():

    layout = [[sg.Text('Introduza o título da publicação que deseja consultar:', key= '-TEXTO-')],
        [sg.Text("Título:", key= "-CONSULTAR_TITLE-"), sg.Input(key= "-CONSULTAR_TITULO-")],
        [sg.Button("Procurar", key= "-PROCURAR_TITULO-"), sg.Button("Cancelar", key= "-CANCELAR_TITULO-")]
    ]
    
    window = sg.Window('Consultar Publicação Por Título', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return

        elif event == '-PROCURAR_TITULO-':

            busca_title = values["-CONSULTAR_TITULO-"].strip()
            
            if busca_title:
               
                publicação = logic.Consultar_Title(publicações, busca_title)
               
                if publicação:
                   
                    detalhes = ["\n=== Detalhes da Publicação ==="]
                    if publicação.get('title'):
                        detalhes.append(f"Título: {publicação['title']}")
                    elif publicação.get('abstract'):
                        detalhes.append(f"Resumo: {publicação['abstract']}")
                    elif publicação.get('keywords'):
                        detalhes.append(f"Palavras-chave: {publicação['keywords']}")
                    elif publicação.get('doi'):
                        detalhes.append(f"DOI: {publicação['doi']}")
                    elif publicação.get('pdf'):
                        detalhes.append(f"PDF: {publicação['pdf']}")
                    elif publicação.get('publish_date'):
                        detalhes.append(f"Data de Publicação: {publicação['publish_date']}")
                    elif publicação.get('url'):
                        detalhes.append(f"URL: {publicação['url']}")
                    
                    detalhes.append("\n--- Autores ---")
                    for autor in publicação.get('authors', []):
                        detalhes.append(
                            f"name: {autor.get('name', 'Nome não disponível')} ::: "
                            f"affiliation: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                            f"orcid: {autor.get('orcid', 'ORCID não disponível')}")

                    detalhes_texto = "\n".join(detalhes) # Juntamos as informações todas dentro da lista de detalhes numa só string

                    window.extend_layout(window, [
                        [sg.Multiline(detalhes_texto, size=(60, 15), disabled=True, key="-DETALHES_PUBLICACAO-")],
                        [sg.Button("Cancelar", key="-CANCELAR_CONSULTAR-")]
                    ])
                   
                else:
                    sg.popup(f'Nenhuma publicação encontrada com o título "{busca_title}".')
            else:
                sg.popup("Por favor, insira um título válido.")

        elif event == '-CANCELAR_TITULO-':
            window.close()
        
        elif event == '-CANCELAR_CONSULTAR-':
            window.close()

def Consultar_PDF_Layout():

    layout = [[sg.Text('Introduza o link do PDF da publicação que deseja consultar:', key= '-TEXTO-')],
        [sg.Text("Link PDF:"), sg.Input(key= "-CONSULTAR_PDF-")],
        [sg.Button("Procurar", key= "-PROCURAR_PDF-"), sg.Button("Cancelar", key= "-CANCELAR_PDF-")]
    ]
    
    window = sg.Window('Consultar Publicação Por PDF', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return

        elif event == '-PROCURAR_PDF-':

            busca_PDF = values["-CONSULTAR_PDF-"].strip()
            
            if busca_PDF:
               
                publicação = logic.Consultar_PDF(publicações, busca_PDF)
               
                if publicação:
                   
                    detalhes = ["\n=== Detalhes da Publicação ==="]
                    if publicação.get('title'):
                        detalhes.append(f"Título: {publicação['title']}")
                    elif publicação.get('abstract'):
                        detalhes.append(f"Resumo: {publicação['abstract']}")
                    elif publicação.get('keywords'):
                        detalhes.append(f"Palavras-chave: {publicação['keywords']}")
                    elif publicação.get('doi'):
                        detalhes.append(f"DOI: {publicação['doi']}")
                    elif publicação.get('pdf'):
                        detalhes.append(f"PDF: {publicação['pdf']}")
                    elif publicação.get('publish_date'):
                        detalhes.append(f"Data de Publicação: {publicação['publish_date']}")
                    elif publicação.get('url'):
                        detalhes.append(f"URL: {publicação['url']}")
                    
                    detalhes.append("\n--- Autores ---")
                    for autor in publicação.get('authors', []):
                        detalhes.append(
                            f"name: {autor.get('name', 'Nome não disponível')} ::: "
                            f"affiliation: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                            f"orcid: {autor.get('orcid', 'ORCID não disponível')}")

                    detalhes_texto = "\n".join(detalhes) # Juntamos as informações todas dentro da lista de detalhes numa só string

                    window.extend_layout(window, [
                        [sg.Multiline(detalhes_texto, size=(60, 15), disabled=True, key="-DETALHES_PUBLICACAO-")],
                        [sg.Button("Cancelar", key="-CANCELAR_CONSULTAR-")]
                    ])
                   
                else:
                    sg.popup(f'Nenhuma publicação encontrada com o link PDF "{busca_PDF}".')
            else:
                sg.popup("Por favor, insira um título válido.")

        elif event == '-CANCELAR_PDF-':
            window.close()
        
        elif event == '-CANCELAR_CONSULTAR-':
            window.close()

def Consultar_DOI_Layout():

    layout = [[sg.Text('Introduza o link do DOI da publicação que deseja consultar:', key= '-TEXTO-')],
        [sg.Text("Link DOI:"), sg.Input(key= "-CONSULTAR_DOI-")],
        [sg.Button("Procurar", key= "-PROCURAR_DOI-"), sg.Button("Cancelar", key= "-CANCELAR_DOI-")]
    ]
    
    window = sg.Window('Consultar Publicação Por DOI', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return

        elif event == '-PROCURAR_DOI-':

            busca_DOI = values["-CONSULTAR_DOI-"].strip()
            
            if busca_DOI:
               
                publicação = logic.Consultar_DOI(publicações, busca_DOI)
               
                if publicação:
                   
                    detalhes = ["\n=== Detalhes da Publicação ==="]
                    if publicação.get('title'):
                        detalhes.append(f"Título: {publicação['title']}")
                    elif publicação.get('abstract'):
                        detalhes.append(f"Resumo: {publicação['abstract']}")
                    elif publicação.get('keywords'):
                        detalhes.append(f"Palavras-chave: {publicação['keywords']}")
                    elif publicação.get('doi'):
                        detalhes.append(f"DOI: {publicação['doi']}")
                    elif publicação.get('pdf'):
                        detalhes.append(f"PDF: {publicação['pdf']}")
                    elif publicação.get('publish_date'):
                        detalhes.append(f"Data de Publicação: {publicação['publish_date']}")
                    elif publicação.get('url'):
                        detalhes.append(f"URL: {publicação['url']}")
                    
                    detalhes.append("\n--- Autores ---")
                    for autor in publicação.get('authors', []):
                        detalhes.append(
                            f"name: {autor.get('name', 'Nome não disponível')} ::: "
                            f"affiliation: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                            f"orcid: {autor.get('orcid', 'ORCID não disponível')}")

                    detalhes_texto = "\n".join(detalhes) # Juntamos as informações todas dentro da lista de detalhes numa só string

                    window.extend_layout(window, [
                        [sg.Multiline(detalhes_texto, size=(60, 15), disabled=True, key="-DETALHES_PUBLICACAO-")],
                        [sg.Button("Cancelar", key="-CANCELAR_CONSULTAR-")]
                    ])
                   
                else:
                    sg.popup(f'Nenhuma publicação encontrada com o link DOI "{busca_DOI}".')
            else:
                sg.popup("Por favor, insira um título válido.")

        elif event == '-CANCELAR_DOI-':
            window.close()
        
        elif event == '-CANCELAR_CONSULTAR-':
            window.close()

def Consultar_URL_Layout():

    layout = [[sg.Text('Introduza o link do URL da publicação que deseja consultar:', key= '-TEXTO-')],
        [sg.Text("Link URL:"), sg.Input(key= "-CONSULTAR_URL-")],
        [sg.Button("Procurar", key= "-PROCURAR_URL-"), sg.Button("Cancelar", key= "-CANCELAR_URL-")]
    ]
    
    window = sg.Window('Consultar Publicação Por URL', layout, finalize=True)

    while True:
        event,values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return

        elif event == '-PROCURAR_URL-':

            busca_URL = values["-CONSULTAR_URL-"].strip()
            
            if busca_URL:
               
                publicação = logic.Consultar_URL(publicações, busca_URL)
               
                if publicação:
                   
                    detalhes = ["\n=== Detalhes da Publicação ==="]
                    if publicação.get('title'):
                        detalhes.append(f"Título: {publicação['title']}")
                    elif publicação.get('abstract'):
                        detalhes.append(f"Resumo: {publicação['abstract']}")
                    elif publicação.get('keywords'):
                        detalhes.append(f"Palavras-chave: {publicação['keywords']}")
                    elif publicação.get('doi'):
                        detalhes.append(f"DOI: {publicação['doi']}")
                    elif publicação.get('pdf'):
                        detalhes.append(f"PDF: {publicação['pdf']}")
                    elif publicação.get('publish_date'):
                        detalhes.append(f"Data de Publicação: {publicação['publish_date']}")
                    elif publicação.get('url'):
                        detalhes.append(f"URL: {publicação['url']}")
                    
                    detalhes.append("\n--- Autores ---")
                    for autor in publicação.get('authors', []):
                        detalhes.append(
                            f"name: {autor.get('name', 'Nome não disponível')} ::: "
                            f"affiliation: {autor.get('affiliation', 'Afiliação não disponível')} ::: "
                            f"orcid: {autor.get('orcid', 'ORCID não disponível')}")

                    detalhes_texto = "\n".join(detalhes) # Juntamos as informações todas dentro da lista de detalhes numa só string

                    window.extend_layout(window, [
                        [sg.Multiline(detalhes_texto, size=(60, 15), disabled=True, key="-DETALHES_PUBLICACAO-")],
                        [sg.Button("Cancelar", key="-CANCELAR_CONSULTAR-")]
                    ])
                   
                else:
                    sg.popup(f'Nenhuma publicação encontrada com o link URL "{busca_URL}".')
            else:
                sg.popup("Por favor, insira um título válido.")

        elif event == '-CANCELAR_URL-':
            window.close()
        
        elif event == '-CANCELAR_CONSULTAR-':
            window.close()

def Listar_Autores_Layout():

    lista_autores  = []

    autor_pub = logic.Listar_Autores(publicações)

    lista_autores = ["---- Lista de Autores ----"]
    for autor, pub in autor_pub.items(): # O método .items() cria uma lista de tuplos que temos de desmembrar
        lista_autores.append(f"\nAutor: {autor}\nPublicações:")
        for title in pub:
            lista_autores.append(f" * {title}")
    
    lista_autores_texto = "\n".join(lista_autores) # Juntamos as informações todas dentro da lista de autores numa só string

    layout = [[sg.Multiline(lista_autores_texto, size=(90, 60), disabled=True, key="-DETALHES_PUBLICACAO-",  autoscroll=True)],
              [sg.Button("Fechar", key="-CANCELAR-")]
              ]
    
    window = sg.Window('Lista de Autores na Base de Dados', layout, finalize=True)

    while True:
        event, _ = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
                window.close()
                return

def Listar_Pub_Autor_Layout():

    layout = [
        [sg.Text("Introduza o nome do autor:", key='-TEXTO_AUTOR-'),sg.Input(key="-BUSCA_AUTOR-", size=(40, 1))], 
        [sg.Button("Procurar", key="-PROCURAR_AUTOR-"), sg.Button("Cancelar", key="-CANCELAR_AUTOR-")],
        [sg.Multiline("", size=(80, 30), disabled=True, key="-DETALHES_PUBLICACOES-", autoscroll=True)]
    ]

    window = sg.Window('Publicações por Autor', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR_AUTOR-'):
            window.close()
            return
        
        elif event == "-PROCURAR_AUTOR-":
            busca_author = values["-BUSCA_AUTOR-"].strip()

            if busca_author:
                lista_publicações = logic.Listar_Pub_Autor(publicações, busca_author)

                lista_publicações_texto = "\n".join(lista_publicações) # Juntamos as informações todas dentro da lista de publicações numa só string

                if lista_publicações_texto == '':
                    sg.popup(f'Nenhuma publicação encontrada para o autor: {busca_author}.')
                else:
                    window["-DETALHES_PUBLICACOES-"].update(lista_publicações_texto)
            else:
                sg.popup("Por favor, insira um nome válido.")

def Listar_Pub_Afil_Layout():

    layout = [
        [sg.Text("Introduza o nome da afiliação:", key='-TEXTO_AFIL-'),sg.Input(key="-BUSCA_AFIL-", size=(40, 1))], 
        [sg.Button("Procurar", key="-PROCURAR_AFIL-"), sg.Button("Cancelar", key="-CANCELAR_AFIL-")],
        [sg.Multiline("", size=(80, 30), disabled=True, key="-DETALHES_PUBLICACOES-", autoscroll=True)]
    ]

    window = sg.Window('Publicações por Afiliação', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR_AFIL-'):
            window.close()
            return
        
        elif event == "-PROCURAR_AFIL-":
            busca_afil = values["-BUSCA_AFIL-"].strip()

            if busca_afil:
                lista_publicações = logic.Listar_Pub_Afil(publicações, busca_afil)

                lista_publicações_texto = "\n".join(lista_publicações) # Juntamos as informações todas dentro da lista de publicações numa só string

                if lista_publicações_texto == '':
                    sg.popup(f'Nenhuma publicação encontrada para a afiliação: {busca_afil}.')
                else:
                    window["-DETALHES_PUBLICACOES-"].update(lista_publicações_texto)
            else:
                sg.popup("Por favor, insira uma afiliação válida.")

def Listar_Pub_PC_Layout():

    layout = [
        [sg.Text("Introduza a palavra-chave:", key='-TEXTO_PC-'),sg.Input(key="-BUSCA_PC-", size=(40, 1))], 
        [sg.Button("Procurar", key="-PROCURAR_PC-"), sg.Button("Cancelar", key="-CANCELAR_PC-")],
        [sg.Multiline("", size=(80, 30), disabled=True, key="-DETALHES_PUBLICACOES-", autoscroll=True)]
    ]

    window = sg.Window('Publicações por Palavra-Chave', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR_PC-'):
            window.close()
            return
        
        elif event == "-PROCURAR_PC-":
            palavra_chave = values["-BUSCA_PC-"].strip()

            if palavra_chave:
                lista_publicações = logic.Listar_Pub_PC(publicações, palavra_chave)

                lista_publicações_texto = "\n".join(lista_publicações) # Juntamos as informações todas dentro da lista de publicações numa só string

                if lista_publicações_texto == '':
                    sg.popup(f'Nenhuma publicação encontrada para a palavra-chave: {palavra_chave}.')
                else:
                    window["-DETALHES_PUBLICACOES-"].update(lista_publicações_texto)
            else:
                sg.popup("Por favor, insira uma palavra-chave válida.")

def Listar_Data_Pub_Layout():

    layout = [
        [sg.Text("Introduza a data de publicação:", key='-TEXTO_DATA-'),sg.Input(key="-BUSCA_DATA-", size=(40, 1))], 
        [sg.Button("Procurar", key="-PROCURAR_DATA-"), sg.Button("Cancelar", key="-CANCELAR_DATA-")],
        [sg.Multiline("", size=(80, 30), disabled=True, key="-DETALHES_PUBLICACOES-", autoscroll=True)]
    ]

    window = sg.Window('Publicações por Data de Publicação', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR_DATA-'):
            window.close()
            return
        
        elif event == "-PROCURAR_DATA-":
            data_pub = values["-BUSCA_DATA-"].strip()

            if data_pub:
                lista_publicações = logic.Listar_Data_Pub(publicações, data_pub)

                lista_publicações_texto = "\n".join(lista_publicações) # Juntamos as informações todas dentro da lista de publicações numa só string

                if lista_publicações_texto == '':
                    sg.popup(f'Nenhuma publicação encontrada para a data de publicação: {data_pub}.')
                else:
                    window["-DETALHES_PUBLICACOES-"].update(lista_publicações_texto)
            else:
                sg.popup("Por favor, insira uma data de publicação válida.")

def Gerar_Gráficos():
    window = sg.Window('Gráficos', [[sg.Text('Escolha o tipo de gráfico que deseja visualizar:')],
                                    [sg.Button('Top 20 Autores', key= '-TOP20A-'), sg.Button('Top 20 Palavras-Chave', key= '-TOP20PC-'), sg.Button('Palavra-Chave Mais Frequente Por Ano', key= '-TOP1PC-')],
                                    [sg.Button('Publicações Por Ano', key= '-PUB_ANO-'), sg.Button('Publicações Por Mês Num Ano', key= '-PUB_MES-'), sg.Button('Publicações de um Autor Por Ano', key= '-PUB_AUTOR-')],
                                    [sg.Button('Cancelar', key= '-CANCELAR-')]])
    
    stop = False
    while stop is False:
        event, _ = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            stop = True

        elif event == '-TOP20A-':
            dist_20A = logic.Distribuição_20A(publicações)
            gd.graf_20A(dist_20A)

        elif event == '-TOP20PC-':
            dist_20PC = logic.Distribuição_20PC(publicações)
            gd.graf_20PC(dist_20PC)

        elif event == '-TOP1PC-':
            dist_PC = logic.Distribuição_PC(publicações)
            gd.graf_PC(dist_PC)

        elif event == '-PUB_ANO-':
            dist_Ano = logic.Distribuição_Ano(publicações)
            gd.graf_Ano(dist_Ano)

        elif event == '-PUB_MES-': # NÃO FUNCIONAM POR CAUSA DOS INPUTS -> ALTERAR INTERFACE DE COMANDO
            dist_Mês = logic.Distribuição_Mês(publicações)
            gd.graf_Mês(dist_Mês)

        elif event == '-PUB_AUTOR-': # NÃO FUNCIONAM POR CAUSA DOS INPUTS -> ALTERAR INTERFACE DE COMANDO
            dist_Autor = logic.Distribuição_Autor(publicações)
            gd.graf_Autor(dist_Autor)

def Gerar_Relatórios():

    layout = [
        [sg.Text('Escolha o tipo de relatório que deseja visualizar:')],
        [sg.Button('Top 20 Autores', key='-TOP20A-'), 
         sg.Button('Top 20 Palavras-Chave', key='-TOP20PC-'), 
         sg.Button('Palavra-Chave Mais Frequente Por Ano', key='-TOP1PC-')],
        [sg.Button('Publicações Por Ano', key='-PUB_ANO-'), 
         sg.Button('Publicações Por Mês Num Ano', key='-PUB_MES-'), 
         sg.Button('Publicações de um Autor Por Ano', key='-PUB_AUTOR-')],
        [sg.Multiline(size=(80, 20), key='-RESULTADOS-', disabled=True, autoscroll=True)],
        [sg.Button('Cancelar', key='-CANCELAR-')]
    ]

    window = sg.Window('Gerar Relatórios', layout, finalize=True)

    while True:
        event, _ = window.read()

        if event in (sg.WIN_CLOSED, '-CANCELAR-'):
            window.close()
            return

        elif event == '-TOP20A-':
            resultados = logic.Distribuição_20A(publicações)
            window['-RESULTADOS-'].update('\n'.join(f"{chave}: {valor}" for chave, valor in resultados.items()))

        elif event == '-TOP20PC-':
            resultados = logic.Distribuição_20PC(publicações)
            window['-RESULTADOS-'].update('\n'.join(f"{chave}: {valor}" for chave, valor in resultados.items()))

        elif event == '-TOP1PC-':
            resultados = logic.Distribuição_PC(publicações)
            window['-RESULTADOS-'].update('\n'.join(f"{chave}: {valor}" for chave, valor in resultados.items()))

        elif event == '-PUB_ANO-':
            resultados = logic.Distribuição_Ano(publicações)
            window['-RESULTADOS-'].update('\n'.join(f"{chave}: {valor}" for chave, valor in resultados.items()))

        elif event == '-PUB_MES-': # NÃO FUNCIONAM POR CAUSA DOS INPUTS -> ALTERAR INTERFACE DE COMANDO
            resultados = logic.Distribuição_Mês(publicações)
            window['-RESULTADOS-'].update('\n'.join(f"{chave}: {valor}" for chave, valor in resultados.items()))

        elif event == '-PUB_AUTOR-': # NÃO FUNCIONAM POR CAUSA DOS INPUTS -> ALTERAR INTERFACE DE COMANDO
            resultados = logic.Distribuição_Autor(publicações)
            window['-RESULTADOS-'].update('\n'.join(f"{chave}: {valor}" for chave, valor in resultados.items()))

def main():

    stop = False  # Controla o loop principal

    # JANELA PRINCIPAL
    window = sg.Window("Consulta e Análise de Publicações Científicas", criar_layout(publicações), finalize=True)

    while not stop:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            stop = True
    
        # Lógica para CRIAR PUB
        elif event == '-CRIAR-':
            Criar_Pub_Layout()

        # Lógica para APAGAR PUB
        elif event == '-APAGAR-':
            Apagar_Pub_Layout_()
        
        # Lógica para RECUPERAR PUB
        elif event == '-RECUPERAR-':
            logic.Recuperar_Pub('pubs_removidas.json')
            sg.popup('As publicações apagadas foram recuperadas com sucesso!')

        # Lógica para IMPORTAR PUB
        elif event == '-IMPORTAR-':
            fexterno = sg.popup_get_file('Selecione o ficheiro JSON',
                                     file_types=(('Ficheiros JSON', '*.json'),)) # O utilizador pode escolher o ficheiro de que deseja importar publicações 
            mensagens_duplicadas = logic.Importar_Pub(fexterno)
            
            for mensagem in mensagens_duplicadas:
                sg.popup(mensagem)
        
        # Lógica para ATUALIZAR PUB
        elif event == '-ATUALIZAR-':
            Atualizar_Pub_Layout()
        
        # Lógica para CONSULTAR TITLE
        elif event == '-CONSULTAR_POR_TITLE-':
            Consultar_Title_Layout()
        
        # Lógica para CONSULTAR PDF
        elif event == '-CONSULTAR_POR_PDF-':
            Consultar_PDF_Layout()
        
        # Lógica para CONSULTAR TITLE
        elif event == '-CONSULTAR_POR_DOI-':
            Consultar_DOI_Layout()
        
        # Lógica para CONSULTAR TITLE
        elif event == '-CONSULTAR_POR_URL-':
            Consultar_URL_Layout()
        
        # Lógica para LISTAR AUTORES
        elif event == '-LISTAR_AUTORES-':
            Listar_Autores_Layout()

        # Lógica para LISTAR PUB AUTOR
        elif event == "-LISTAR_PUB_AUTOR-":
            Listar_Pub_Autor_Layout()
        
        # Lógica para LISTAR PUB AFILIAÇÃO
        elif event == "-LISTAR_PUB_AFIL-":
            Listar_Pub_Afil_Layout()
        
        # Lógica para LISTAR PUB PC
        elif event == "-LISTAR_PUB_PC-":
            Listar_Pub_PC_Layout()
        
        # Lógica para LISTAR PUB DATA
        elif event == '-LISTAR_DATA_PUB-':
            Listar_Data_Pub_Layout()

        # Lógica para GERAR GRÁFICOS
        elif event == '-GRAFICOS-':
            Gerar_Gráficos()

        # Lógica para GERAR RELATÓRIOS
        elif event == '-RELATORIOS-':
            Gerar_Relatórios()

    window.close()

if __name__ == "__main__":
    main()
