import base64
from base64 import b64decode
import datetime
import io
import tempfile
from urllib.parse import quote as urlquote
import urllib

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


def return_tables():
    '''
     - Apresenta ao usuário o conteúdo da lista de entidades e da lista de relações
     - Também permite o download das duas listas
    
     :Return: html.Div com o conteúdo que será apresentado na tela do usuário
    '''
    df_entidades = pd.read_csv("./csv/lista_entidades.csv")
    df_relacoes = pd.read_csv("./csv/lista_relacoes.csv")
    list_of_tables = []
        
    if df_relacoes.shape[0] > 0 :
        
        csv_string_entidades = df_entidades.to_csv(index=False, encoding='utf-8')
        csv_string_entidades = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string_entidades)

        csv_string_relacoes = df_relacoes.to_csv(index=False, encoding='utf-8')
        csv_string_relacoes = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string_relacoes)

        '''download_button = html.A(
            children=['Download CSV'],
            id='download-link',
            download="visnote_annotations.csv",
            href=csv_string_entidades,
            target="_blank")
        '''
            
        list_of_tables.append(\
            html.Div([
                html.H2("Anotações de Entidades", className='text-act'),
                html.H4("Quantidade: " + str(df_entidades.shape[0]), className='text-ocu'),

                dash_table.DataTable(
                    data=df_entidades.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_entidades.columns],
                    style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': '150px',
                            'height':'auto'
                    }, 
                    style_table={
                            'maxHeight': '700px',
                            'overflowY': 'auto',
                            'overflowX': 'auto',
                            'marginBottom': '40px'
                        }
                ),
                html.A(
                    className = 'choose-button',
                    children=['Download CSV'],
                    id='download-link-entidades',
                    download="visnote_annotations_entidades.csv",
                    href=csv_string_entidades,
                    target="_blank"),
            ], className='card-csv')\
        )
        list_of_tables.append(\
            html.Div([
                html.H2("Anotações de Relações", className='text-act'),
                html.H4("Quantidade: " + str(df_relacoes.shape[0]), className='text-ocu'),

                dash_table.DataTable(
                    data=df_relacoes.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_relacoes.columns],
                    style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': '150px',
                            'height':'auto'
                    }, 
                    style_table={
                            'maxHeight': '700px',
                            'overflowY': 'auto',
                            'overflowX': 'auto',
                            'marginBottom': '40px'
                        }
                ),
                html.A(
                    className = 'choose-button',
                    children=['Download CSV'],
                    id='download-link-relacoes',
                    download="visnote_annotations_relacoes.csv",
                    href=csv_string_relacoes,
                    target="_blank"),
            ], className='card-csv')\
        )
    else:
        list_of_tables.append(\
            html.Div([
                html.H2('Não foram encontradas anotações nos arquivos xml. Por favor, tente novamente.', className='text-act'),
            ], className='card-csv')\
        )

    return html.Div(list_of_tables)

# Função principal (a que contém os callbacks e que será chamada na main.py)   
def export_callbacks(app):
    @app.callback(
        [
            Output('output-anotacoes-revisadas', 'children'),
        ],
        [
            Input("button-output-anotacoes", "n_clicks"),
        ])
    def update_output(run):
        children = []
        if run:
            children = [return_tables()]
        return [children]
