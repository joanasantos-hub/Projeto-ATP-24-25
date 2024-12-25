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
