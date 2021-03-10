from extract_xml import extrair_anotacoes, organize_content, return_tables, return_entidades
from run_multiproj import projecao_multi

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import plotly.express as px
import re

from urllib.parse import quote as urlquote
import urllib

colors = {
        'Ato_Abono_Permanencia': 'rgb(237,100,90)',
        'Ato_Aposentadoria': 'rgb(135,197,95)',
        'Ato_Cessao': 'rgb(15,133,84)',
        'Ato_Exoneracao_Comissionado': 'rgb(180,151,231)',
        'Ato_Exoneracao_Efetivo': 'rgb(220,176,242)',
        'Ato_Nomeacao_Comissionado': 'rgb(102,197,204)',
        'Ato_Nomeacao_Efetivo': 'reg(158,185,243)',
        'Ato_Retificacao_Comissionado': 'rgb(248,156,116)',
        'Ato_Retificacao_Efetivo': 'rgb(246,207,113)',
        'Ato_Reversao': 'rgb(47,138,196)',
        'Ato_Substituicao': 'rgb(254,136,177)',
        'Ato_Tornado_Sem_Efeito_Apo': 'rgb(139,224,164)',
        'Ato_Tornado_Sem_Efeito_Exo_Nom': 'rgb(201,219,116)',
        'Confirmado': '#000000',
        'Avaliar_Depois': 'rgb(179,179,179)',
        'Apagar': '#FFFFFF',
}

def create_layout(app):
    return html.Div([
    html.Link(href="https://fonts.googleapis.com/css2?family=Raleway&display=swap", rel="stylesheet"),
    html.Div([
        # Header
        html.Div(
            className="row header",
            id="app-header",
            children=[
                # Logo do Projeto KnEDLe
                html.Img(
                    src=app.get_asset_url("knedle-logo4.png"),
                    className="logo",
                    id="logo",
                ),

                # Botões para a próxima etapa
                html.Div(
                    className="row background",
                    id="proximo",
                    children=[
                        html.Button(children=["<- Voltar"], className="Button", id="voltar-extrair-classes-button", n_clicks=0),
                        html.Button(children=["Corrigir classes ->"], className="Button", id="corrigir-classes-button", n_clicks=0),
                        html.Button(id="value-corrigir-classes-button", className="Button",n_clicks=0, style={"display":"none"}),
                        html.Button(children=["<- Voltar"], className="Button", id="voltar-corrigir-classes-button", n_clicks=0),
                        html.Button(children=["Extrair entidades ->"], className="Button", id="extrair-entidades-button", n_clicks=0),
                        html.Button(children=["Corrigir entidades ->"], className="Button", id="corrigir-entidades-button", n_clicks=0),
                        ],         
                ),

                # Canto esquerdo do Header
                html.Div(
                    style={"display": "flex"},
                    children=[
                        # Botão para mostrar mini tutorial escrito e um botão para o tutorial em vídeo
                        html.Button(
                            "Ajuda",
                            id="about-button",
                        ),

                        # Logo do VisNote       
                        html.H3(
                            "VisNote 2.0",
                            id="app-title",
                        ),
                    ]
                ),
        ]),

        # Ajuda (ainda precisa ser editado)
        html.Div(
            className="card",
            id="about-us",
            children=[
                html.Div(
                    id="about-content",
                    children=[
                        html.H4(className='card-title',
                                style={"text-align": "center"},
                                children=["About Us"],
                                ),
                        html.Div(id="about-text",
                                 children=[
                                    html.H6("The scatter plot below is the result of running the t-SNE algorithm on DODF's datasets, resulting in 2D and 3D visualizations of the documents."),
                                    html.H6("Official publications such as the Diario Oficial do Distrito Federal (DODF) are sources of information on all official government acts. Although these documents are rich in knowledge, analysing these texts manually by specialists is a complex and unfeasible task considering the growing volume of documents, the result of the frequent number of publications in the Distrito Federal Government's (GDF) communication vehicle."),
                                    html.H6("VisNote aims to facilitate the visualization of such information using unsupervised machine learning methods and data visualization techniques. This is one of the tools developed by the KnEDLe Project. To learn more about us, click on 'Learn More' below.")
                            ]),
                        html.Br(),
                        html.Button(children=[
                            html.A("Learn More", href='https://unb-knedle.github.io/', target="_blank", id="learn-more-button")], className="Button"),
                    ]),
                html.Hr(),
            ],
        ),

        # página de extração de anotações
        html.Div(id = "pagina-extrair-classes",children =[
            # Local para a inserção dos arquivos XML
            html.Div([
                html.H1('Extrair anotações', className='card-title'),
                html.H2('Extração das anotações feitas no NidoTat', className='card-subtitle'),
                html.H2('e armazenadas em arquivos XML', className='card-subtitle'),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        html.Img(src='assets/img/file.svg', className='card-logo-pdf'),
                        html.H3('Arraste e solte o XML aqui', className='text-pdf'),
                        html.Button('Selecione no seu Computador', className='choose-button')
                    ], className='card-pdf-box'),
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
            ], className='card'),
            
            #Onde aparece as anotações que foram extraídas, com a opção de salvá-las em um arquivo CSV
            html.Div(id='output-data-upload')], className='row'),
        ]),

        # página de correção de anotações - nível tipo dos atos
        html.Div(
            className="row background",
            id="pagina-corrigir-classes",
            style={
                       "display": "none",
                       "grid-template-columns": "auto 400px",
                       "height":"auto",
                       },
            children=[
                html.Div(
                    className="card-ato",
                    id="lista atos",
                    children=[
                        html.Div(
                            id="atos",
                            children=[
                                html.H4(className='card-title',
                                        style={"text-align": "center"},
                                        children=["Atos"],
                                        ),  

                                html.Button(id="flag-warning-atos", className="Button",n_clicks=0, style={"display":"none"}),

                                dcc.ConfirmDialog(
                                    id='warning_atos',
                                    message='Não foram encontrados atos pertencentes a esta classe. Por favor, selecione outra(s) classe(s).',
                                ), 
                                
                                dcc.Dropdown(
                                                id="dropdown-atos",
                                                searchable=True,
                                                clearable=False,
                                                multi=True,
                                                options=[
                                                    {"label": "Todos","value": "Todos",},
                                                    {"label": "Ato_Abono_Permanencia","value": "Ato_Abono_Permanencia",}, 
                                                    {"label": "Ato_Cessao","value": "Ato_Cessao",}, 
                                                    {"label": "Ato_Exoneracao_Comissionado","value": "Ato_Exoneracao_Comissionado",}, 
                                                    {"label": "Ato_Exoneracao_Efetivo","value": "Ato_Exoneracao_Efetivo",}, 
                                                    {"label": "Ato_Nomeacao_Comissionado","value": "Ato_Nomeacao_Comissionado",}, 
                                                    {"label": "Ato_Nomeacao_Efetivo","value": "Ato_Nomeacao_Efetivo",}, 
                                                    {"label": "Ato_Retificacao_Comissionado","value": "Ato_Retificacao_Comissionado",}, 
                                                    {"label": "Ato_Retificacao_Efetivo","value": "Ato_Retificacao_Efetivo",},
                                                    {"label": "Ato_Reversao","value": "Ato_Reversao",}, 
                                                    {"label": "Ato_Substituicao","value": "Ato_Substituicao",}, 
                                                    {"label": "Ato_Tornado_Sem_Efeito_Apo","value": "Ato_Tornado_Sem_Efeito_Apo",},                                                                    
                                                    {"label": "Ato_Tornado_Sem_Efeito_Exo_Nom","value": "Ato_Tornado_Sem_Efeito_Exo_Nom",},
                                                    {"label": "Apagar","value": "Apagar",}, 
                                                    {"label": "Avaliar Depois","value": "Avaliar_Depois",}, 
                                                ],
                                                placeholder="Select a class",
                                                value="Todos",
                                ),

                                html.Div(id='tabela_atos',children=[
                                    dash_table.DataTable(
                                        id='datatable',
                                        #columns=[{"name": i, "id": i} for i in df2.columns],
                                        #data=df2.to_dict('records'),
                                        editable=True,
                                        row_selectable="single",
                                        selected_rows=[],
                                        hidden_columns=['x_tsne','y_tsne','x_umap','y_umap','cod','documento','id','anotador','estado'],
                                        css=[{"selector": ".show-hide", "rule": "display: none", }],
                                        style_as_list_view=True,
                                        style_cell={
                                                'overflow': 'auto',
                                                'textOverflow': 'ellipsis',
                                                'minWidth':'300px',
                                                #'maxWidth': '300px',
                                                'textAlign': 'left'
                                        }, 
                                        style_data={
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                        },
                                        style_table={
                                                'maxHeight': '67vh',
                                                'overflowY': 'auto',
                                                'overflowX': 'auto',
                                                #'marginBottom': '40px'
                                        },
                                        style_header={
                                            #'display': 'none'
                                        },
                                    ),
                                ])
                                             
                        ]),    
                    ],
                ),
                #menu e layout
                html.Div(
                    id="pagina-corrigir-classes-meio",
                    #style={"height": "100%"},
                    children=[
                        # menu com os controles
                        html.Div(
                            className="row background",
                            id="menu",
                            children=[
                                html.Div(
                                    id="menu-visualizacoes",
                                    children=[
                                        dcc.Dropdown(
                                            id="dropdown-method",
                                            searchable=False,
                                            clearable=False,
                                            options=[
                                                {"label": "UMAP","value": "UMAP",},
                                                {"label": "t-SNE","value": "t-SNE",},                                                                    
                                            ],
                                            placeholder="Select a technique",
                                            value="UMAP",
                                        ),
                                        dcc.Dropdown(
                                            id="dropdown-label",
                                            searchable=False,
                                            clearable=False,
                                            options=[
                                                {"label": "Classe","value": "classe",},
                                                {"label": "Estado","value": "estado",},                                                                    
                                            ],
                                            placeholder="Select a label",
                                            value="estado",
                                        ),
                                        html.Button("vários",id="confirmar-varios-classes-button", className="Button",n_clicks=0),
                                        html.Button(id="confirmar-varios-classes-button-result", className="Button",n_clicks=0,style={"display":"none"}),
                                        html.A(children=[html.Button("Salvar",id="salvar-corrigir-classes-button", className="Button",n_clicks=0)],
                                            id='salvar-corrigir-classes-link',
                                            download="backup_classes.csv",
                                            href="",
                                            target="_blank",
                                        ),                           
                                    ]
                                ),
                            ],
                        ),
                        
                        # Layouts
                        html.Div(className='card-graph', id = "grafico",
                            children=[
                                dcc.Graph(id="graph-3d-plot-tsne")
                            ]),
                ]),
                
                # telas que mostram informações extras sob demanda
                html.Div(
                    id="control-tabs",
                    children=[
                        dcc.Tabs(id='tabs', value='point', children=[
                            # guia referente às informações do ponto que foi clicado por último
                            dcc.Tab(
                                label='ATO SELECIONADO',
                                value='point',
                                children=[
                                    html.Div(id='control-tab', style={"padding": "5px"}, children=[
                                        html.Div(id="selected-point"),
                                        html.Div(id="corrigir-classe-buttons", children=[
                                            html.Button("confirmar",id="confirmar-classe-button", className="Button",n_clicks=0),
                                            html.Button(id="confirmar-classe-button-result", className="Button",n_clicks=0, style={"display":"none"}), 
                                            html.Button("corrigir",id="corrigir-classe-button", className="Button",n_clicks=0),
                                        ]),                  
                                        html.Div(id="input-corrigir-classe",children=[
                                            html.H6("Nova classe:"),
                                            html.H6(className="card-tab",children=[
                                                dcc.Dropdown(
                                                id="dropdown-classes",
                                                searchable=True,
                                                clearable=False,
                                                options=[
                                                    {"label": "Ato_Abono_Permanencia","value": "Ato_Abono_Permanencia",},
                                                    {"label": "Ato_Aposentadoria","value": "Ato_Aposentadoria",}, 
                                                    {"label": "Ato_Cessao","value": "Ato_Cessao",}, 
                                                    {"label": "Ato_Exoneracao_Comissionado","value": "Ato_Exoneracao_Comissionado",}, 
                                                    {"label": "Ato_Exoneracao_Efetivo","value": "Ato_Exoneracao_Efetivo",}, 
                                                    {"label": "Ato_Nomeacao_Comissionado","value": "Ato_Nomeacao_Comissionado",}, 
                                                    {"label": "Ato_Nomeacao_Efetivo","value": "Ato_Nomeacao_Efetivo",}, 
                                                    {"label": "Ato_Retificacao_Comissionado","value": "Ato_Retificacao_Comissionado",},
                                                    {"label": "Ato_Retificacao_Efetivo","value": "Ato_Retificacao_Efetivo",}, 
                                                    {"label": "Ato_Reversao","value": "Ato_Reversao",}, 
                                                    {"label": "Ato_Substituicao","value": "Ato_Substituicao",}, 
                                                    {"label": "Ato_Tornado_Sem_Efeito_Apo","value": "Ato_Tornado_Sem_Efeito_Apo",},                                                                    
                                                    {"label": "Ato_Tornado_Sem_Efeito_Exo_Nom","value": "Ato_Tornado_Sem_Efeito_Exo_Nom",},
                                                    {"label": "Apagar","value": "Apagar",}, 
                                                    {"label": "Avaliar Depois","value": "Avaliar_Depois",}, 
                                                ],
                                                placeholder="Select a class",
                                                value="Ato_Cessao",
                                            ),
                                            ]),
                                            html.Button("Enviar",id="enviar-corrigir-classe-button", className="Button",n_clicks=0),
                                            html.Button(id="enviar-corrigir-classe-button-result",n_clicks=0, style={"display":"none"}),
                                        ]),
                                ]),
                                
                            ]),

                            dcc.Tab(
                                label='LEGENDA CORES',
                                value='legend',
                                children=[
                                    html.Div(id='control-tab-2', style={"padding": "10px", 'width':'40vh'}, children=[
                                    html.H6("Classes:"),
                                    #html.P(style={'display':'grid','grid-template-columns':'25% 75%', 'float':'left'},children=[html.P('#',style={'color':'rgb(237,100,90)'}),"Ato_Abono_Permanencia"]),
                                    html.P("Ato_Abono_Permanencia"),
                                    html.P("Ato_Aposentadoria"),
                                    html.P("Ato_Exoneracao_Comissionado"),
                                    html.P("Ato_Exoneracao_Efetivo"),
                                    html.P("Ato_Abono_Permanencia"),
                                    html.P("Ato_Nomeacao_Comissionado"),
                                    html.P("Ato_Nomeacao_Efetivo"),
                                    html.P("Ato_Retificacao_Comissionado"),
                                    html.P("Ato_Retificacao_Efetivo"),
                                    html.P("Ato_Reversao"),
                                    html.P("Ato_Substituicao"),
                                    html.P("Ato_Tornado_Sem_Efeito_Apo"),
                                    html.P("Ato_Tornado_Sem_Efeito_Exo_Nom"),
                                    html.Br(),
                                    html.H6("Estados:"),
                                    html.P("Confirmado: a classe deste ato já foi verificada"),
                                    html.P("Apagar: o conteúdo desta anotação não é um ato"),
                                    html.P("Avaliar Depois:o anotador está em dúvida sobre a classe"),
                                    ])
                                ]
                            ),                                
                        ])
                    ]
                ),
            ],
        ),

        # página de extração de entidades
        html.Div(id = "pagina-extrair-entidades",children =[
            #Onde aparecem várias tabelas, uma para cada tipo de ato, com as entidades que foram extraídas
            html.Div(id='output-entidades')], className='row'
        ),
])

def main_callbacks(app):

    #Geral

    @app.callback(
        [
            Output("about-us", "style")   
        ],
        [
            Input("about-button", "n_clicks")
        ]
    )
    def display_about(clicks):
        if clicks is None:
            clicks = 0
        if (clicks % 2) == 1:
            clicks += 1
            return [{}]
        else:
            clicks += 1 

        return [{"display": "none"}]

    @app.callback(
        [ 
            Output("corrigir-classes-button", "style"),   
            Output("pagina-extrair-classes", "style"),
            Output("voltar-extrair-classes-button", "style"),
            Output("extrair-entidades-button", "style"),   
            Output("pagina-corrigir-classes", "style"),
            Output("voltar-corrigir-classes-button", "style"), 
            Output("corrigir-entidades-button", "style"),   
            Output("pagina-extrair-entidades", "style"),
        ],
        [
            Input('upload-data', 'contents'),
            Input("corrigir-classes-button", "n_clicks"),
            Input("extrair-entidades-button", "n_clicks"), 
            Input("voltar-extrair-classes-button", "n_clicks"),
            Input("voltar-corrigir-classes-button", "n_clicks"),
        ]
    )
    def control_displays(upload_data,corrigir_classes,extrair_entidades,voltar_extrair_classes,voltar_corrigir_classes):

        if voltar_corrigir_classes > 0:
            return [{"display":"none"}, # corrigir-classes-button
                    {"display":"none"}, # pagina-extrair-classes
                    {},
                    {}, # extrair-entidades-button
                    {"padding": "15px","display": "grid","grid-template-columns": "400px auto 400px","height": "100vh"}, #pagina-corrigir-classes
                    {"display":"none"},
                    {"display":"none"}, # corrigir-entidades-button
                    {"display": "none"}] # pagina-extrair-entidades
        
        elif extrair_entidades > 0:
            return [{"display":"none"}, # corrigir-classes-button
                    {"display":"none"}, # pagina-extrair-classes
                    {"display":"none"},
                    {"display":"none"}, # extrair-entidades-button
                    {"display":"none"}, # pagina-corrigir-classes
                    {},
                    {}, # corrigir-entidades-button
                    {}] # pagina-extrair-entidades
        
        elif voltar_extrair_classes > 0:
            return [{}, #corrigir-classes-button
                    {}, #pagina-extrair-classes
                    {"display":"none"},
                    {"display":"none"}, # extrair-entidades-button
                    {"display": "none"}, #pagina-corrigir-classes
                    {"display":"none"},
                    {"display":"none"}, #corrigir-entidades-button
                    {"display": "none"}] #pagina-extrair-entidades

        elif corrigir_classes > 0:
            return [{"display":"none"}, # corrigir-classes-button
                    {"display":"none"}, # pagina-extrair-classes
                    {},
                    {}, # extrair-entidades-button
                    {"padding": "15px","display": "grid","grid-template-columns": "400px auto 400px","height": "100vh"}, #pagina-corrigir-classes
                    {"display":"none"},
                    {"display":"none"}, # corrigir-entidades-button
                    {"display": "none"}] # pagina-extrair-entidades
        elif (upload_data is not None):
            return [{}, #corrigir-classes-button
                    {}, #pagina-extrair-classes
                    {"display":"none"},
                    {"display":"none"}, # extrair-entidades-button
                    {"display": "none"}, #pagina-corrigir-classes
                    {"display":"none"},
                    {"display":"none"}, #corrigir-entidades-button
                    {"display": "none"}] #pagina-extrair-entidades
        return [{"display": "none"}, #corrigir-classes-button
                {}, #pagina-extrair-classes
                {"display":"none"},
                {"display":"none"}, # extrair-entidades-button
                {"display": "none"}, #pagina-corrigir-classes
                {"display":"none"},
                {"display":"none"}, #corrigir-entidades-button
                {"display": "none"}] #pagina-extrair-entidades

    @app.callback(
        [ 
            Output("voltar-extrair-classes-button", "n_clicks"),
            Output("voltar-corrigir-classes-button", "n_clicks"),
        ],
        [
            Input('upload-data', 'contents'),
            Input("corrigir-classes-button", "n_clicks"),
            Input("extrair-entidades-button", "n_clicks"), 
        ]
    )
    def reset_voltar_buttons(upload_data,corrigir_classes,extrair_entidades):
        return [0, 0]

    
    # Extrair anotações XML - Parte 1

    @app.callback(
        [
            Output('output-data-upload', 'children'),
        ],
        [
            Input('upload-data', 'contents')
        ],
        [
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified')
        ])
    def update_output(list_of_contents, list_of_names, list_of_dates):
        children = []
        if list_of_contents is not None:
            xmls = []
            organize_content(list_of_contents, list_of_names, list_of_dates,xmls)
            modo = "junto"
            children = [return_tables(xmls,modo)]
            return [children]
        
        return [children]

    @app.callback(
        [
            Output('output-entidades', 'children'),
        ],
        [
            Input("extrair-entidades-button", "n_clicks"),
        ],
        [
            State('upload-data', 'contents'),
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified')
        ])
    def update_output(extrair, list_of_contents, list_of_names, list_of_dates):
        children = []
        if extrair:
            xmls = []
            organize_content(list_of_contents, list_of_names, list_of_dates,xmls)
            children = [return_entidades(xmls)]
            return [children]
        
        return [children]

    # Corrigir Classes

    # Gráfico

            #color_discrete_sequence=px.colors.qualitative.Pastel
    def generate_figure(dict_dfs, mp,label):
        if mp == "TEMP" and label == "estado":
            figure = px.scatter(dict_dfs, x='x_umap', y='y_umap', color = "estado",
                                color_discrete_map=colors)
        elif mp == 'UMAP' and label == "estado":
            figure = px.scatter(dict_dfs, x='x_umap', y='y_umap', color = "estado",
                                color_discrete_map=colors)
        elif mp == 't-SNE' and label == "estado":
            figure = px.scatter(dict_dfs, x='x_tsne', y='y_tsne', color = "estado", 
                                color_discrete_map=colors)
        elif mp == 'UMAP' and label == "classe":
            figure = px.scatter(dict_dfs, x='x_umap', y='y_umap', color = "tipo",
                                color_discrete_map=colors)
        elif mp == 't-SNE' and label == "classe":
            figure = px.scatter(dict_dfs, x='x_tsne', y='y_tsne', color = "tipo", 
                                color_discrete_map=colors)

        figure.update_traces(marker=dict(line=dict(width=1, color='white')),)

        figure.update_layout(legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1,
            title=dict(text="Legenda", font=dict(
                family="Arial", size=22), side="top"),
            valign="top",
            itemclick="toggleothers",
        ),
            yaxis={'visible': False, 'showticklabels': False},
            xaxis={'visible': False, 'showticklabels': False},
            margin=dict(l=40, r=40, t=50, b=40))

        figure.update_layout(showlegend=False)
        return figure

    @app.callback(
        [    
            Output("value-corrigir-classes-button", "n_clicks"),
        ],
        [
            Input("corrigir-classes-button", "n_clicks")
        ]    
    )
    def run_tsne_umap(run):
        if run > 0:
            df = pd.read_csv("testando.csv")
            dict_dfs = projecao_multi(df) 
            dict_dfs.to_csv("testando_tsne_umap.csv",index=False)
            return [1]
        return [0]

    @app.callback(
        [
            Output('warning_atos', 'displayed'),
        ],
        [
            Input("flag-warning-atos", 'n_clicks')
        ]
    )
    def display_confirm(value):
        if value == 1:
            return [True]
        return [False]

    @app.callback(
        [
            Output('tabela_atos', 'children'),
        ],
        [
            Input("dropdown-atos","value"),
            Input("value-corrigir-classes-button", "n_clicks"),
        ]
    )
    def update_styles(tipos,run):
        if run == 0:
            df = pd.read_csv("temp_df.csv")
        else:
            df = pd.read_csv("testando_tsne_umap.csv")
        
        df2 = df
        if "Todos" not in tipos:
            df2 = df[(df.estado == tipos[0])]
            if len(tipos) > 1:
                t = len(tipos)
                j = 1
                while j < t:
                    df3 = df[(df.estado == tipos[j])]
                    j = j + 1
                    frames = [df2,df3]
                    df2 = pd.concat(frames)

        temp = df2.tipo
        df2 = df2.drop(columns=['tipo'])
        df2["tipo"] = temp

        return [
            dash_table.DataTable(
                id='datatable',
                columns=[
                    {"name": i, "id": i} for i in df2.columns
                ],
                data=df2.to_dict('records'),
                editable=True,
                row_selectable="single",
                selected_rows=[],
                hidden_columns=['x_tsne','y_tsne','x_umap','y_umap','cod','documento','id','anotador','estado'],
                css=[{"selector": ".show-hide", "rule": "display: none", }],
                style_as_list_view=True,
                style_cell={
                        'overflow': 'auto',
                        'textOverflow': 'ellipsis',
                        'minWidth':'300px',
                        #'maxWidth': '300px',
                        'textAlign': 'left'
                }, 
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_table={
                        'maxHeight': '67vh',
                        'overflowY': 'auto',
                        'overflowX': 'auto',
                        #'marginBottom': '40px'
                },
                style_header={
                    #'display': 'none'
                },
            ),
        ]

    @app.callback(
        [    
            Output("graph-3d-plot-tsne", "figure"),
            Output("flag-warning-atos", 'n_clicks'),
        ],
        [
            Input("dropdown-atos","value"),
            Input("value-corrigir-classes-button", "n_clicks"),
            Input("dropdown-method", "value"),
            Input("dropdown-label", "value"),
            Input("confirmar-classe-button-result", "n_clicks"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input("confirmar-varios-classes-button-result", "n_clicks")
        ]    
    )
    def display_scatter_plot(tipos,run,mp,label,confirmar,enviar,confirmar_varios):
        #tipos = ["Ato_Substituicao", "Ato_Nomeacao_Comissionado",'Ato_Retificacao_Comissionado','Ato_Tornado_Sem_Efeito_Apo', "Ato_Tornado_Sem_Efeito_Exo_Nom"]
        display = 0
        if run == 0:
            df = pd.read_csv("temp_df.csv")
            figure = generate_figure(df,'TEMP',label)

        elif run > 0 or confirmar > 0 or enviar > 0 or confirmar_varios > 0:
            df = pd.read_csv("testando_tsne_umap.csv")
            df2 = df
            if "Todos" not in tipos:
                df2 = df[(df.estado == tipos[0])]
                if len(df2) == 0:
                    display = 1
                    figure = generate_figure(df,mp,label)
                    return [figure,display]
                if len(tipos) > 1:
                    t = len(tipos)
                    j = 1
                    while j < t:
                        df3 = df[(df.estado == tipos[j])]
                        j = j + 1
                        frames = [df2,df3]
                        df2 = pd.concat(frames)
                
            figure = generate_figure(df2,mp,label)
            return [figure,display]

        return [figure,display]

    # Interações

    @app.callback(
        [
            Output("corrigir-classe-buttons","style"),
            Output("input-corrigir-classe","style"),
        ],
        [
            Input("corrigir-classe-button","n_clicks"),
            Input("enviar-corrigir-classe-button","n_clicks"),
            Input("graph-3d-plot-tsne", "clickData"),
            Input('datatable', "derived_virtual_selected_rows")
        ]
    )
    def display_corrigir(corrigir,enviar,clickData,clickTable):
        if clickTable is None:
            clickTable = []

        if (not clickData) and clickTable == []: 
            return[{"display":"none"},{"display":"none"}]
        elif corrigir == enviar:
            return [{},{"display":"none"}]
        elif corrigir > enviar:
            return [{"display":"none"},{}]
        
        return [{},{}]


    def achar_indice(clickData,mp):
        df = pd.read_csv("testando_tsne_umap.csv")

        XY = {}
        XY['x'] = clickData["points"][0]['x']
        XY['y'] = clickData["points"][0]['y']

        X = []
        X.append(XY['x'])
        Y = []
        Y.append(XY['y'])
        
        if mp == 'UMAP':
            indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index
                    
        elif mp == 't-SNE':
            indice = df[(df['x_tsne'].isin(X)) & (df['y_tsne'].isin(Y))].index

        else: 
            indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index

        return indice

    def achar_indice_tabela_atos(x,y):
        df = pd.read_csv("testando_tsne_umap.csv")

        XY = {}
        XY['x'] = x
        XY['y'] = y

        X = [x]
        #X.append(XY['x'])
        Y = [y]
        #Y.append(XY['y'])
        
        
        indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index

        return indice

    @app.callback(
        [
            #Output("enviar-corrigir-classe-button-result", "n_clicks"),
            Output("dropdown-classes","value")
        ],
        [
            Input("corrigir-classe-button", "n_clicks"),
        ],
        [
            State("graph-3d-plot-tsne", "clickData"),
            State("dropdown-method", "value")
        ]
    )
    def corrigir_classe(corrigir,clickData,mp):
        result = 0
        label = "Apagar"
        if corrigir > 0:
            df = pd.read_csv("testando_tsne_umap.csv")

            indice = achar_indice(clickData,mp)

            label = str(df['tipo'][indice])

            result = 1

            return [label]

        return [label]

    @app.callback(
        [
            Output("enviar-corrigir-classe-button-result", "n_clicks"),
        ],
        [
            Input("enviar-corrigir-classe-button", "n_clicks"),
        ],
        [
            State("dropdown-classes","value"),
            State("graph-3d-plot-tsne", "clickData"),
            State("dropdown-method", "value")
        ]
    )
    def corrigir_classe(enviar,classe,clickData,mp):
        result = 0
        if enviar > 0:
            df = pd.read_csv("testando_tsne_umap.csv")

            indice = achar_indice(clickData,mp)

            label = df['tipo'][indice]

            
            if classe == "Avaliar_Depois":
                df.at[indice, 'estado'] = "Avaliar_Depois"
            elif classe == "Apagar":
                df.at[indice, 'estado'] = "Apagar"
                df.at[indice, 'tipo'] = "Apagar"
            else: 
                df.at[indice, 'tipo'] = classe
                df.at[indice, 'estado'] = "Confirmado"
            

            df.to_csv("testando_tsne_umap.csv",index=False)

            result = 1

            return [result]

        return [result]

    @app.callback(
        [    
            Output("confirmar-classe-button-result", "n_clicks"),
        ],
        [
            Input("confirmar-classe-button", "n_clicks")
        ],
        [
            State("graph-3d-plot-tsne", "clickData"),
            State("dropdown-method", "value")
        ]    
    )
    def confirmar_classe(confirmar,clickData,mp):
        result = 0
        if confirmar > 0:
            df = pd.read_csv("testando_tsne_umap.csv")

            indice = achar_indice(clickData,mp)

            df.at[indice, 'estado'] = "Confirmado"

            df.to_csv("testando_tsne_umap.csv",index=False)

            result = 1

            return [result]

        return [result]

    @app.callback(
        [
            Output("selected-point", "children"),
        ],
        [
            Input("graph-3d-plot-tsne", "clickData"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input('datatable', "derived_virtual_selected_rows")
        ],
        [
            State("dropdown-method", "value"),
            State('datatable', "data"),
        ]
    )
    def explore_data(clickData,enviar, selected_row_indices, mp, table):
        df = pd.read_csv("testando_tsne_umap.csv")
        label = 'Apagar'
        contents = []

        contents.append(html.H5("Clique em um ponto no layout para obter mais informações."),)

        if selected_row_indices is None:
            selected_row_indices = []

        if selected_row_indices != []:
            selected_rows=[table[i] for i in selected_row_indices]
            x = selected_rows[0]["x_umap"]
            y = selected_rows[0]["y_umap"]

            indice = achar_indice_tabela_atos(x,y)

            contents = []
            label = df['tipo'][indice]
            conteudo = df['conteudo'][indice]
            documento = df['documento'][indice]
            idd = df['id'][indice]
    
            contents.append(html.H6("Classe atual:"))
            for j in label:
                contents.append(html.P(j,className="card-tab"))
            contents.append(html.H6("Ato:"))
            for i in conteudo:
                contents.append(html.P(i,className="card-tab"))
            contents.append(html.H6("Documento:"))
            for k in documento:
                contents.append(html.P(k,className="card-tab"))
            contents.append(html.H6("Id:"))
            for l in idd:
                contents.append(html.P(l,className="card-tab"))

        if clickData or enviar:
            indice = achar_indice(clickData,mp)

            # Retrieve the index of the point clicked, given it is present in the set
            
            contents = []
            label = df['tipo'][indice]
            conteudo = df['conteudo'][indice]
            documento = df['documento'][indice]
            idd = df['id'][indice]
    
            contents.append(html.H6("Classe atual:"))
            for j in label:
                contents.append(html.P(j,className="card-tab"))
            contents.append(html.H6("Ato:"))
            for i in conteudo:
                contents.append(html.P(i,className="card-tab"))
            contents.append(html.H6("Documento:"))
            for k in documento:
                contents.append(html.P(k,className="card-tab"))
            contents.append(html.H6("Id:"))
            for l in idd:
                contents.append(html.P(l,className="card-tab"))

        return [contents]

    @app.callback(
        [
            Output("confirmar-varios-classes-button-result", "n_clicks")
        ],
        [
            Input("confirmar-varios-classes-button", "n_clicks"),
        ],
        [
            State("graph-3d-plot-tsne", "selectedData"),
            State("dropdown-method", "value")
        ]
    )
    def confirmar_classe_varios(confirmar, selectedData, mp):
        df = pd.read_csv("testando_tsne_umap.csv")

        if selectedData:
            
            j = 0
            for point in selectedData["points"]:
                XY = {}
                XY['x'] = selectedData["points"][j]['x']
                XY['y'] = selectedData["points"][j]['y']

                X = []
                X.append(XY['x'])
                Y = []
                Y.append(XY['y'])
                
                if mp == 'UMAP':
                    indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index
                            
                elif mp == 't-SNE':
                    indice = df[(df['x_tsne'].isin(X)) & (df['y_tsne'].isin(Y))].index

                else: 
                    indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index

                df.at[indice, 'estado'] = "Confirmado"
                j += 1

            df.to_csv("testando_tsne_umap.csv",index=False)

            return [1]

        '''
        i = 0
        qnt = 0
        while i < len(df):
            if df["estado"][i] == "Confirmado":
                qnt += 1
            i += 1
        '''

        return [0]

    @app.callback(
        [
            Output('salvar-corrigir-classes-link', 'href'),
        ],
        [
            Input("salvar-corrigir-classes-button", 'n_clicks'),
        ]
    )
    def salvar_corrigir_classes(salvar):
        csv_string = ""

        if salvar:
            df = pd.read_csv("testando_tsne_umap.csv")
            dff = df
            csv_string = dff.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8," + \
                urllib.parse.quote(csv_string)
        return [csv_string]
    
