import PySimpleGUI as sg
import json
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from collections import defaultdict

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

        [sg.Button("Criar Publicação", key="-CRIAR-")],
        [sg.Button("Atualizar Publicação", key="-ATUALIZAR-")],
        [sg.Button("Apagar Publicação", key="-APAGAR-")],
        [sg.Button("Recuperar Publicações Apagadas", key="-RECUPERAR-")],
        [sg.Button("Consultar Por Título", key="-CONSULTAR_TITLE-")],
        [sg.Button("Consultar Por PDF", key="-CONSULTAR_PDF-")],
        [sg.Button("Consultar Por DOI", key="-CONSULTAR_DOI-")],
        [sg.Button("Consultar Por URL", key="-CONSULTAR_URL-")],
        [sg.Button("Consultar Autores", key="-LISTAR_AUTORES-")],
        [sg.Button("Consultar Por Autor", key="-LISTAR_PUB_AUTOR-")],
        [sg.Button("Consultar Por Afiliação", key="-LISTAR_PUB_AFIL-")],
        [sg.Button("Consultar Por Data", key="-LISTAR_PUB_DATA-")],
        [sg.Button("Consultar Por Palavra-Chave", key="-LISTAR_PUB_PC-")],
        [sg.Button("Gerar Relatórios", key= "-RELATORIOS-")],
        [sg.Button("Gerar Gráficos", key="-GRAFICOS-")],
        [sg.Button("Importar Publicações", key="-IMPORTAR-")]

    ]

    bloco_visualização = [
            [sg.Column(
            layout=[
                [sg.Text("Consulta e Análise de Publicações Científicas", key="-PAINEL-")],
                [sg.Multiline(size=(80, 40), key="-Dados-", autoscroll=True, disabled=True)]
            ],
            element_justification="center",
            justification="center",
            expand_x=True,
            expand_y=True,
            key="-COLUNA_VISUALIZACAO-"
        )],
    ]

    layout = [
        [
            sg.Column(menu_botoes),
            sg.VSeperator(),  # Separador vertical
            sg.Column(bloco_visualização, element_justification="center", key="-COLUNA_VISUALIZACAO-")
        ],
    ]
    return layout

# Layout Para Criar Nova Publicação
def Criar_Pub_Layout():
    
    layout = [
        [sg.Text("Título:"), sg.Input(key="-TITULO-")],
        [sg.Text("Palavras-chave:"), sg.Input(key="-KEYWORDS-")],
        [sg.Text("Resumo:"), sg.Multiline(size=(50, 5), key="-ABSTRACT-")],
        [sg.Text("Data de Publicação (A-M-D):"), sg.Input(key="-DATA-")],
        [sg.Text("DOI:"), sg.Input(key="-DOI-")],
        [sg.Text("PDF:"), sg.Input(key="-PDF-")],
        [sg.Text("URL:"), sg.Input(key="-URL-")],
        [sg.Text("Autores (Nome, Afiliação, ORCID separados por vírgula):")],
        [sg.Multiline(size=(50, 5), key="-AUTORES-")],
        [sg.Button("Salvar", key="-SALVAR_PUBLICACAO-"), sg.Button("Cancelar", key="-CANCELAR_PUBLICACAO-")]
    ]
    return layout

# Processamento de Informação de Cada Autor
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

def Gerar_Gráficos():
       window = sg.Window('Gráficos', [[sg.Text('Escolha o tipo de gráfico que deseja visualizar:')],
                                        [sg.Button('Top 20 Autores'), sg.Button('Top 20 Palavras-Chave'), sg.Button('Palavra-Chave Mais Frequente Por Ano')],
                                        [sg.Button('Publicações Por Ano'), sg.Button('Publicações Por Mês Num Ano'), sg.Button('Publicações de um Autor Por Ano')],
                                        [sg.Button('Cancelar')]])
       
       while True:
            event, _ = window.read()

            if event in (sg.WIN_CLOSED, 'Cancelar'):
                window.close()
                return

            elif event == 'Top 20 Autores':

                dist_20A = logic.Distribuição_20A(publicações)
                gd.graf_20A(dist_20A)

            elif event == 'Top 20 Palavras-Chave':
                dist_20PC = logic.Distribuição_20PC(publicações)
                gd.graf_20PC(dist_20PC)

            elif event == 'Palavra-Chave Mais Frequente Por Ano':
                dist_PC = logic.Distribuição_PC(publicações)
                gd.graf_PC(dist_PC)

            elif event == 'Publicações Por Ano': # NÃO FUNCIONAM POR CAUSA DOS INPUTS -> ALTERAR INTERFACE DE COMANDO
                dist_Ano = logic.Distribuição_Ano(publicações)
                gd.graf_Ano(dist_Ano)

            elif event == 'Publicações Por Mês': # NÃO FUNCIONAM POR CAUSA DOS INPUTS -> ALTERAR INTERFACE DE COMANDO
                dist_Mês = logic.Distribuição_Mês(publicações)
                gd.graf_Mês(dist_Mês)

            elif event == 'Publicações de um Autor Por Ano':
                dist_Autor = logic.Distribuição_Autor(publicações)
                gd.graf_Autor(dist_Autor)
            window.close()

def Gerar_Relatório():
    window = sg.Window('Gerar Relatórios', [[sg.Text('Escolha o tipo de relatório que deseja visualizar:')],
                                        [sg.Button('Top 20 Autores'), sg.Button('Top 20 Palavras-Chave'), sg.Button('Palavra-Chave Mais Frequente Por Ano')],
                                        [sg.Button('Publicações Por Ano'), sg.Button('Publicações Por Mês Num Ano'), sg.Button('Publicações de um Autor Por Ano')],
                                        [sg.Button('Cancelar')]])

    while True:
        event, _ = window.read()

        if event in (sg.WIN_CLOSED, 'Cancelar'):
            window.close()
            return

        elif event == 'Relatório de Publicações por Autor':
            logic.Listar_Pub_Autor(publicações)
        elif event == 'Relatório de Publicações por Afiliação':
            logic.Listar_Pub_Afil(bd)
        window.close()

def main():

    stop = False  # Controla o loop principal
    pub_adicionada = False  # Verifica se a nova publicação foi adicionada à base de dados

    # Cria a janela principal
    window = sg.Window("Consulta e Análise de Publicações Científicas", criar_layout(publicações), finalize=True)

    while not stop:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            stop = True

        # Lógica para criar publicação
        if event == "-CRIAR-":

            if not pub_adicionada:
                # Adiciona os campos de criação ao painel
                window.extend_layout(
                    window["-COLUNA_VISUALIZACAO-"],
                    Criar_Pub_Layout()
                )
                pub_adicionada = True
            window["-Dados-"].update(visible=False)

        # Lógica para salvar publicação
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
            
            # Remove os campos de criação de publicação e restaura o painel
            for key in ["-TITULO-", "-KEYWORDS-", "-ABSTRACT-", "-DATA-", "-DOI-", "-PDF-", "-URL-", "-AUTORES-"]:
                if key in window.key_dict:
                    window[key].update(visible=False)
            pub_adicionada = False

            # Restaura o painel original
            window.refresh()  # Força a atualização da interface
            window["-Dados-"].update(visible=True)

        # Lógica para cancelar a criação da publicação
        elif event == "-CANCELAR_PUBLICACAO-":
            # Remove os campos de criação de publicação
            for key in ["-TITULO-", "-KEYWORDS-", "-ABSTRACT-", "-DATA-", "-DOI-", "-PDF-", "-URL-", "-AUTORES-"]:
                if key in window.key_dict:
                    window[key].update(visible=False)
            pub_adicionada = False

            # Restaura o painel original
            window.refresh()  # Força a atualização da interface
            window["-Dados-"].update(visible=True)
        
        elif event == '-GRAFICOS-':
            Gerar_Gráficos()

    window.close()

if __name__ == "__main__":
    main()
