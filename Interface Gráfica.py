import PySimpleGUI as sg
import json
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
from collections import defaultdict

#import interface_cmd as logic  ?????

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

