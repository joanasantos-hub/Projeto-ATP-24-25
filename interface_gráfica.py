import PySimpleGUI as sg
import json
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from collections import defaultdict

# import interface_cmd as logic ???? No module named

publicacoes = [] # Lista de dicionários

sg.theme('LightPurple') # Definir o tema

# _________________________________________________________________ INTERFACE GRÁFICA _________________________________________________________________________

def hoje():
    # Retorna a data atual
    return datetime.today().date()


def criar_layout(publicacoes):

    menu_botoes = [
        [sg.Button("Criar Publicação", key="-CRIAR-")],
        [sg.Button("Consultar Publicação", key="-CONSULTAR-")],
        [sg.Button("Listar Publicações", key="-LISTARPUBS-")],
        [sg.Button("Atualizar Publicação", key="-ATUALIZAR-")],
        [sg.Button("Eliminar Publicação", key="-ELIMINAR-")],
        [sg.Button("Ver Publicações Eliminadas", key="-ELIMINADAS-")],
        [sg.Button("Gerar Relatório", key= "-RELATORIO-")],
        [sg.Button("Gerar Gráfico", key="-GRAFICO-")],
        [sg.Button("Listar Autores", key="-LISTARAUTORES-")],
        [sg.Button("Importar Publicações", key="-IMPORTAR-")],
        [sg.Button("Guardar Publicações", key="-GUARDAR-")],
        [sg.Button("Help", key= "-HELP-")],
        [sg.Button("Sair", key="-SAIR-")]
    ]

    bloco_visualizacao = [
        [sg.Text("Consulta e Análise de Publicações Científicas", key="-PAINEL-")],
        [sg.Multiline(size=(60, 30), key="-Dados-", autoscroll=True, disabled=True)],
    ]

    layout = [
        [
            sg.Column(menu_botoes),
            sg.VSeperator(),  # Separador vertical
            sg.Column(bloco_visualizacao)
        ],
    ]
    return layout

# Criação de uma nova publicação

def criacao(): 
    global publicacoes

# Carregar publicações existentes

    publicacoes = logic.Carregar_BD()

    layout_publicacoes = [
        [sg.Text("Introduza o resumo da publicação:")],
        [sg.InputText(key='-ABSTRACT-')],
        [sg.Text("Introduza palavras-chave da publicação (separadas por vírgula):")],
        [sg.InputText(key='-KEYWORDS-')],
        [sg.Text("Introduza a data da publicação (A-M-D):")],
        [sg.InputText(key='-DATA-', readonly=True), sg.CalendarButton('Escolher Data', target='-DATA-', format='%d/%m/%Y')],
        [sg.Text("Introduza o doi da publicação:")],
        [sg.InputText(key='-DOI-')],
        [sg.Text("Introduza o pdf da publicação:")],
        [sg.InputText(key='-PDF-')],
        [sg.Text("Introduza o título da publicação:")],
        [sg.InputText(key='-TITLE-')],
        [sg.Text("Introduza o url da publicação:")]
        [sg.Button('Criar Publicação'), sg.Button('Cancelar')]

    ]


    authors = []
    novos_authors = True  
    while novos_authors:
        name = sg.popup_get_text("Introduza o nome do autor (ou deixe em branco para terminar):")
        if not name:
            novos_authors = False  
        else:
            affiliation = sg.popup_get_text(f"Introduza a afiliação de {name}:")
            orcid = sg.popup_get_text(f"Introduza o ORCID de {name}:")
            authors.append({"name": name, "affiliation": affiliation, "orcid": orcid})

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

    # Adicionar a nova publicação ao banco de dados
    publicacoes.append(nova_pub)
    with open('ata_medica_papers.json', 'w', encoding='utf-8') as f:
        json.dump(publicacoes, f, ensure_ascii=False, indent=4)

    sg.popup("Publicação Criada com Sucesso!")


# Função para consultar a publicação por título
def consultar_publicacao(publicacoes):
    busca_title = sg.popup_get_text("Introduza o título da publicação que deseja consultar:")
    for publicação in publicacoes:
        if publicação.get('title') and publicação['title'].lower() == busca_title.lower():
            detalhes = f"Título: {publicação['title']}\n"
            if publicação.get('abstract'):
                detalhes += f"Resumo: {publicação['abstract']}\n"
            if publicação.get('keywords'):
                detalhes += f"Palavras-chave: {publicação['keywords']}\n"
            if publicação.get('doi'):
                detalhes += f"DOI: {publicação['doi']}\n"
            if publicação.get('pdf'):
                detalhes += f"PDF: {publicação['pdf']}\n"
            if publicação.get('publish_date'):
                detalhes += f"Data de Publicação: {publicação['publish_date']}\n"
            if publicação.get('url'):
                detalhes += f"URL: {publicação['url']}\n"
            detalhes += "\n--- Autores ---\n"
            for autor in publicação['authors']:
                detalhes += f"Nome: {autor.get('name', 'Nome não disponível')} ::: " \
                            f"Afiliação: {autor.get('affiliation', 'Afiliação não disponível')} ::: " \
                            f"ORCID: {autor.get('orcid', 'ORCID não disponível')}\n"
            sg.popup("Detalhes da Publicação", detalhes)
            return
    sg.popup("Nenhuma publicação encontrada com o título fornecido.")

# Função para apagar a publicação
def apagar_publicacao(publicacoes):
    title = sg.popup_get_text("Insira o título da publicação que deseja apagar:")
    publicacoes = [pub for pub in publicacoes if pub['title'] != title]
    with open('ata_medica_papers.json', 'w', encoding='utf-8') as f:
        json.dump(publicacoes, f, ensure_ascii=False, indent=4)
    sg.popup("Publicação apagada com sucesso!")

# Função principal para criar a janela e gerenciar os eventos
def main():
    try:
        with open('ata_medica_papers.json', 'r', encoding='utf-8') as f:
            publicacoes = json.load(f)
    except FileNotFoundError:
        publicacoes = []

    layout = criar_layout(publicacoes)
    window = sg.Window("Gestão de Publicações", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "-SAIR-":
            break
        elif event == "-CRIAR-":
            criar_publicacao(publicacoes)
        elif event == "-CONSULTAR-":
            consultar_publicacao(publicacoes)
        elif event == "-APAGAR-":
            apagar_publicacao(publicacoes)

    window.close()

# Executar o programa
if __name__ == "__main__":
    main()
