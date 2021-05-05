from extraction import extraction_callbacks, organize_content, return_tables
from multidimensional_projection import projecao_multi
from export import export_callbacks

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

from ast import literal_eval

colors = {
        'Ato_Abono_Permanencia': 'rgb(237,100,90)',
        'Ato_Aposentadoria': 'rgb(135,197,95)',
        'Ato_Cessao': 'rgb(15,133,84)',
        'Ato_Exoneracao_Comissionado': 'rgb(180,151,231)',
        'Ato_Exoneracao_Efetivo': 'rgb(220,176,242)',
        'Ato_Nomeacao_Comissionado': 'rgb(102,197,204)',
        'Ato_Nomeacao_Efetivo': 'rgb(158,185,243)',
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

options_entidades = [{'label': 'Ato_Abono_Permanencia', 'value': 'Ato_Abono_Permanencia'},
 {'label': 'Ato_Exoneracao_Comissionado','value': 'Ato_Exoneracao_Comissionado'},
 {'label': 'Ato_Exoneracao_Efetivo', 'value': 'Ato_Exoneracao_Efetivo'},
 {'label': 'Ato_Nomeacao_Comissionado', 'value': 'Ato_Nomeacao_Comissionado'},
 {'label': 'Ato_Retificacao_Comissionado','value': 'Ato_Retificacao_Comissionado'},
 {'label': 'Ato_Retificacao_Efetivo', 'value': 'Ato_Retificacao_Efetivo'},
 {'label': 'Ato_Tornado_Sem_Efeito_Exo_Nom','value': 'Ato_Tornado_Sem_Efeito_Exo_Nom'},
 {'label': 'nome', 'value': 'nome'},
 {'label': 'simbolo', 'value': 'simbolo'},
 {'label': 'cargo_comissionado', 'value': 'cargo_comissionado'},
 {'label': 'hierarquia_lotacao', 'value': 'hierarquia_lotacao'},
 {'label': 'orgao', 'value': 'orgao'},
 {'label': 'a_pedido_ou_nao', 'value': 'a_pedido_ou_nao'},
 {'label': 'motivo', 'value': 'motivo'},
 {'label': 'matricula', 'value': 'matricula'},
 {'label': 'tipo_documento', 'value': 'tipo_documento'},
 {'label': 'data_documento', 'value': 'data_documento'},
 {'label': 'numero_dodf', 'value': 'numero_dodf'},
 {'label': 'data_dodf', 'value': 'data_dodf'},
 {'label': 'pagina_dodf', 'value': 'pagina_dodf'},
 {'label': 'cargo_efetivo', 'value': 'cargo_efetivo'},
 {'label': 'vigencia', 'value': 'vigencia'},
 {'label': 'quadro', 'value': 'quadro'},
 {'label': 'processo_SEI', 'value': 'processo_SEI'},
 {'label': 'informacao_errada', 'value': 'informacao_errada'},
 {'label': 'informacao_corrigida', 'value': 'informacao_corrigida'},
 {'label': 'tipo_ato', 'value': 'tipo_ato'},
 {'label': 'lotacao', 'value': 'lotacao'},
 {'label': 'matricula_SIAPE', 'value': 'matricula_SIAPE'},
 {'label': 'fundamento_legal', 'value': 'fundamento_legal'},
 {'label': 'numero_documento', 'value': 'numero_documento'},
 {'label': 'Ato_Substituicao', 'value': 'Ato_Substituicao'},
 {'label': 'nome_substituto', 'value': 'nome_substituto'},
 {'label': 'matricula_substituto', 'value': 'matricula_substituto'},
 {'label': 'cargo_substituto', 'value': 'cargo_substituto'},
 {'label': 'nome_substituido', 'value': 'nome_substituido'},
 {'label': 'matricula_substituido', 'value': 'matricula_substituido'},
 {'label': 'simbolo_objeto_substituicao','value': 'simbolo_objeto_substituicao'},
 {'label': 'cargo_objeto_susbtituicao', 'value': 'cargo_objeto_susbtituicao'},
 {'label': 'data_inicial', 'value': 'data_inicial'},
 {'label': 'data_final', 'value': 'data_final'},
 {'label': 'numero_dodf_edital_normativo','value': 'numero_dodf_edital_normativo'},
 {'label': 'data_dodf_edital_normativo','value': 'data_dodf_edital_normativo'},
 {'label': 'numero_dodf_resultado_final','value': 'numero_dodf_resultado_final'},
 {'label': 'data_dodf_resultado_final', 'value': 'data_dodf_resultado_final'},
 {'label': 'cargo', 'value': 'cargo'},
 {'label': 'edital_normativo', 'value': 'edital_normativo'},
 {'label': 'edital_resultado_final', 'value': 'edital_resultado_final'},
 {'label': 'candidato', 'value': 'candidato'},
 {'label': 'Ato_Nomeacao_Efetivo', 'value': 'Ato_Nomeacao_Efetivo'},
 {'label': 'simbolo_substituto', 'value': 'simbolo_substituto'},
 {'label': 'Ato_Tornado_Sem_Efeito_Apo','value': 'Ato_Tornado_Sem_Efeito_Apo'},
 {'label': 'padrao', 'value': 'padrao'},
 {'label': 'classe', 'value': 'classe'},
 {'label': 'orgao_cedente', 'value': 'orgao_cedente'},
 {'label': 'cargo_orgao_cessionario', 'value': 'cargo_orgao_cessionario'},
 {'label': 'orgao_cessionario', 'value': 'orgao_cessionario'},
 {'label': 'Ato_Cessao', 'value': 'Ato_Cessao'},
 {'label': 'onus', 'value': 'onus'},
 {'label': 'Ato_Reversao', 'value': 'Ato_Reversao'},
 {'label': 'matricula_siape', 'value': 'matricula_siape'},
 {'label': 'data_edital_normativo', 'value': 'data_edital_normativo'},
 {'label': 'data_edital_resultado_final','value': 'data_edital_resultado_final'},
 {'label': 'carreira', 'value': 'carreira'},
 {'label': 'data', 'value': 'data'}]

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
                        html.Button(children=["<- Voltar"], className="Button", id="voltar-extrair-classes-button", n_clicks=0, style={"display":"none"}),
                        html.Button(children=["Revisar anotações ->"], className="Button", id="corrigir-classes-button", n_clicks=0, style={"display":"none"}),
                        html.Button(id="value-corrigir-classes-button", className="Button",n_clicks=0, style={"display":"none"}),
                        html.Button(children=["<- Voltar"], className="Button", id="voltar-corrigir-classes-button", n_clicks=0, style={"display":"none"}),
                        html.Button(children=["Exportar anotações ->"], className="Button", id="extrair-entidades-button", n_clicks=0, style={"display":"none"}),
                        html.Button(children=["Corrigir entidades ->"], className="Button", id="corrigir-entidades-button", n_clicks=0, style={"display":"none"}),
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
            style={"display": "none"},
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
                    #className="card-ato",
                    id="lista_atos",
                    className="control-tabs",
                    children=[                       
                        dcc.Tabs(id='tabs_left', value='atos', children=[
                            # guia referente às informações do ponto que foi clicado por último
                            dcc.Tab(
                                label='ATOS',
                                value='atos',
                                children=[                                    
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
                                        id='datatable_relacoes',
                                        #columns=[{"name": i, "id": i} for i in df2.columns],
                                        #data=df2.to_dict('records'),
                                        editable=False,
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

                            dcc.Tab(
                                label='ENTIDADES',
                                value='entidades',
                                children=[
                                    html.Div(id='tabela_entidades',children=[
                                    dash_table.DataTable(
                                        id='datatable_entidades',
                                        #columns=[{"name": i, "id": i} for i in df2.columns],
                                        #data=df2.to_dict('records'),
                                        editable=False,
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
                                ]
                            ),

                            #guia legenda
                            dcc.Tab(
                                label='LEGENDA',
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
                    ],
                ),
                #menu e layout
                html.Div(
                    id="pagina-corrigir-classes-meio",
                    className="control-tabs",
                    
                    children=[
                        dcc.Tabs(id='tabs_middle', value='atos_graph', 
                    #style={"height": "100%"},
                        children=[
                            dcc.Tab(
                                label='RELAÇÕES',
                                value='atos_graph',
                                children=[
                                    # Layouts className='card-graph',
                                    html.Div( id = "grafico",
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
                                                            value="t-SNE",
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
                                                            value="classe",
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
                                            dcc.Graph(id="graph-3d-plot-tsne")
                                        ]),
                                ]),
                            dcc.Tab(
                                label='ENTIDADES',
                                value='entidades_graph',
                                children=[
                                    # Layouts className='card-graph',
                                    html.Div(id = "grafico-entidades",
                                        children=[
                                        # menu com os controles
                                        html.Div(
                                            className="row background",
                                            id="menu-entidades",
                                            children=[
                                                html.Div(
                                                    id="menu-visualizacoes-entidades",
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="dropdown-method-entidades",
                                                            searchable=False,
                                                            clearable=False,
                                                            options=[
                                                                {"label": "UMAP","value": "UMAP",},
                                                                {"label": "t-SNE","value": "t-SNE",},                                                                    
                                                            ],
                                                            placeholder="Select a technique",
                                                            value="t-SNE",
                                                        ),
                                                        dcc.Dropdown(
                                                            id="dropdown-label-entidades",
                                                            searchable=False,
                                                            clearable=False,
                                                            options=[
                                                                {"label": "Classe","value": "classe",},
                                                                {"label": "Estado","value": "estado",},                                                                    
                                                            ],
                                                            placeholder="Select a label",
                                                            value="classe",
                                                        ),
                                                        html.Button("vários",id="confirmar-varios-entidades-button", className="Button",n_clicks=0),
                                                        html.Button(id="confirmar-varios-entidades-button-result", className="Button",n_clicks=0,style={"display":"none"}),
                                                        html.A(children=[html.Button("Salvar",id="salvar-corrigir-entidades-button", className="Button",n_clicks=0)],
                                                            id='salvar-corrigir-entidades-link',
                                                            download="backup_entidades.csv",
                                                            href="",
                                                            target="_blank",
                                                        ),                           
                                                    ]
                                                ),
                                            ],
                                        ),
                                            dcc.Graph(id="graph-entidades")
                                        ]),
                                ]),
                        ]),
                ]),
                
                # telas que mostram informações extras sob demanda
                html.Div(
                    className="control-tabs",
                    
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
                                            html.Button("confirmar",id="confirmar-classe-button", className="Button",n_clicks=0,style={"display":"none"}),
                                            html.Button(id="confirmar-classe-button-result", className="Button",n_clicks=0, style={"display":"none"}), 
                                            html.Button("corrigir",id="corrigir-classe-button", className="Button",n_clicks=0,style={"display":"none"}),
                                        ]),                  
                                        html.Div(id="input-corrigir-classe",style={"display":"none"},children=[
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
                                            html.Button("Enviar",id="enviar-corrigir-classe-button", className="Button",n_clicks=0,style={"display":"none"}),
                                            html.Button(id="enviar-corrigir-classe-button-result",n_clicks=0, style={"display":"none"}),
                                        ]),
                                ]),
                                
                            ]),
                            
                            
                                                            
                        ])
                    ]
                ),
            ],
        ),

        # página de exportação de anotações revisadas
        html.Div(id = "pagina-extrair-entidades",children =[
            #Onde aparecem várias tabelas, uma para cada tipo de ato, com as entidades que foram extraídas
            html.Div(id='output-anotacoes-revisadas')], className='row'
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
        '''
        return [{"display":"none"}, # corrigir-classes-button
                    {"display":"none"}, # pagina-extrair-classes
                    {"display":"none"},
                    {"display":"none"}, # extrair-entidades-button
                    {"padding": "15px","display": "grid","grid-template-columns": "400px auto 400px","height": "100vh"}, #pagina-corrigir-classes
                    {"display":"none"},
                    {"display":"none"}, # corrigir-entidades-button
                    {"display": "none"}] # pagina-extrair-entidades
        '''
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

    
    # Parte 1 - Extração de anotações do XML
    extraction_callbacks(app)

    export_callbacks(app)
    
    '''
    @app.callback(
        [
            Output('output-anotacoes-revisadas', 'children'),
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
    '''

    # multidimensional projection callbacks

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
            relacoes = pd.read_csv("./csv/lista_relacoes.csv")
            mdp_relacoes = projecao_multi(relacoes) 
            mdp_relacoes.to_csv("./csv/lista_relacoes.csv",index=False)
            entidades = pd.read_csv("./csv/lista_entidades.csv")
            mdp_entidades = projecao_multi(entidades) 
            mdp_entidades.to_csv("./csv/lista_entidades.csv",index=False)

            return [1]
        return [0]

    #layout e layout enrichments callbacks

    def generate_figure(dict_dfs, mp,label,ent_ou_rel):
        if mp == 'TEMP' or mp == 'UMAP':
            X = 'x_umap'
            Y = 'y_umap'
        else: 
            X = 'x_tsne'
            Y = 'y_tsne'

        if ent_ou_rel == 'ent':
            if label == 'classe':
                COLOR = 'tipo_ent'
            else:
                COLOR = 'estado_ent'

            figure = px.scatter(dict_dfs, x=X, y=Y,hover_name='texto', color = COLOR,color_discrete_sequence=px.colors.qualitative.Pastel)
            figure.update_layout(legend=dict(orientation="v",yanchor="top",y=1,xanchor="left",x=1,title=dict(text="Legenda", font=dict(family="Arial", size=22), side="top"),valign="top",itemclick="toggleothers",),yaxis={'visible': False, 'showticklabels': False},xaxis={'visible': False, 'showticklabels': False},margin=dict(l=40, r=40, t=50, b=40))

        elif ent_ou_rel == 'rel':
            if label == 'classe':
                COLOR = 'tipo_rel'
            else:
                COLOR = 'estado_rel'
            
            figure = px.scatter(dict_dfs, x=X, y=Y, color = COLOR,color_discrete_map=colors)
            figure.update_layout(showlegend=False)

        figure.update_traces(marker=dict(line=dict(width=1, color='white')),)
            
        return figure

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
    def montar_tabela_relacoes(tipos,run):
        if run == 0:
            df = pd.read_csv("./csv/relacoes_temp.csv")
        else:
            df = pd.read_csv("./csv/lista_relacoes.csv")
        
        df2 = df
        if "Todos" not in tipos:
            df2 = df[(df.tipo_rel == tipos[0])]
            if len(tipos) > 1:
                t = len(tipos)
                j = 1
                while j < t:
                    df3 = df[(df.tipo_rel == tipos[j])]
                    j = j + 1
                    frames = [df2,df3]
                    df2 = pd.concat(frames)

        #ajustando o posicionamento das colunas, não afeta nada em questão de valores
        temp = df2.tipo_rel
        df2 = df2.drop(columns=['tipo_rel'])
        df2["tipo_rel"] = temp

        temp = df2.tipo_rel
        df2 = df2.drop(columns=['estado_rel'])
        df2["estado_rel"] = temp

        return [
            dash_table.DataTable(
                id='datatable_relacoes',
                columns=[
                    {"name": i, "id": i} for i in df2.columns
                ],
                data=df2.to_dict('records'),
                editable=False,
                row_selectable="single",
                selected_rows=[],
                hidden_columns=['id_geral','id_dodf_rel','anotacoes','x_tsne','y_tsne','x_umap','y_umap'],
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
            Output('tabela_entidades', 'children'),
        ],
        [
            Input("dropdown-atos","value"),
            Input("value-corrigir-classes-button", "n_clicks"),
        ]
    )
    def montar_tabela_entidades(tipos,run):
        if run == 0:
            df = pd.read_csv("./csv/entidades_temp.csv")
        else:
            df = pd.read_csv("./csv/lista_entidades.csv")
        
        df2 = df[(df.tipo_rel != df.tipo_ent)]
        
        if "Todos" not in tipos:
            df2 = df[(df.tipo_rel == tipos[0])]
            if len(tipos) > 1:
                t = len(tipos)
                j = 1
                while j < t:
                    df3 = df[(df.tipo_rel == tipos[j])]
                    j = j + 1
                    frames = [df2,df3]
                    df2 = pd.concat(frames)

        #ajustando o posicionamento das colunas, não afeta nada em questão de valores
        temp = df2.tipo_ent
        df2 = df2.drop(columns=['tipo_ent'])
        df2["tipo_ent"] = temp

        temp = df2.tipo_rel
        df2 = df2.drop(columns=['tipo_rel'])
        df2["tipo_rel"] = temp

        temp = df2.estado_ent
        df2 = df2.drop(columns=['estado_ent'])
        df2["estado_ent"] = temp

        return [
            dash_table.DataTable(
                id='datatable_entidades',
                columns=[
                    {"name": i, "id": i} for i in df2.columns
                ],
                data=df2.to_dict('records'),
                editable=False,
                row_selectable="single",
                selected_rows=[],
                hidden_columns= ['id_geral', 'id_dodf_rel', 'id_dodf', 'id_rel','anotador_rel', 'id_ent', 'anotador_ent','x_tsne', 'y_tsne', 'x_umap', 'y_umap'],
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
    def display_grafico_relacoes(tipos,run,mp,label,confirmar,enviar,confirmar_varios):
        display = 0
        if run == 0:
            df = pd.read_csv("./csv/relacoes_temp.csv")
            figure = generate_figure(df,'TEMP',label,'rel')
        elif run > 0 or confirmar > 0 or enviar > 0 or confirmar_varios > 0:
            df = pd.read_csv("./csv/lista_relacoes.csv")
            
            df2 = df
            if "Todos" not in tipos:
                df2 = df[(df.tipo_rel == tipos[0])]
                if len(df2) == 0:
                    display = 1
                    figure = generate_figure(df,mp,label,'rel')
                    return [figure,display]
                if len(tipos) > 1:
                    t = len(tipos)
                    j = 1
                    while j < t:
                        df3 = df[(df.tipo_rel == tipos[j])]
                        j = j + 1
                        frames = [df2,df3]
                        df2 = pd.concat(frames)
            
                
            figure = generate_figure(df2,mp,label,'rel')

        return [figure,display]

    @app.callback(
        [    
            Output("graph-entidades", "figure"),
        ],
        [
            Input("dropdown-atos","value"),
            Input("value-corrigir-classes-button", "n_clicks"),
            Input("dropdown-method-entidades", "value"),
            Input("dropdown-label-entidades", "value"),
            Input("confirmar-classe-button-result", "n_clicks"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input("confirmar-varios-entidades-button-result", "n_clicks")
        ]    
    )
    def display_grafico_entidades(tipos,run,mp,label,confirmar,enviar,confirmar_varios):
        display = 0
        if run == 0:
            df = pd.read_csv("./csv/entidades_temp.csv")
            figure = generate_figure(df,'TEMP',label,'ent')
        elif run > 0 or confirmar > 0 or enviar > 0 or confirmar_varios > 0:
            df = pd.read_csv("./csv/lista_entidades.csv")
            
            df2 = df
            if "Todos" not in tipos:
                df2 = df[(df.tipo_rel == tipos[0])]
                if len(df2) == 0:
                    display = 1
                    figure = generate_figure(df,mp,label,'ent')
                    return [figure,display]
                if len(tipos) > 1:
                    t = len(tipos)
                    j = 1
                    while j < t:
                        df3 = df[(df.tipo_rel == tipos[j])]
                        j = j + 1
                        frames = [df2,df3]
                        df2 = pd.concat(frames)
            
                
            figure = generate_figure(df2,mp,label,'ent')

        return [figure]


    # Interações

    # Parte referente a atualizar 'detail on demand' de acordo com interações nas tabelas e gráficos 
    # (falta atualizações de qnd ocorrer alterações nas anotações)

    def find_id_tabela(id_dodf_rel):
        df = pd.read_csv("./csv/lista_relacoes.csv")
        indice = df[df.id_dodf_rel == id_dodf_rel].index

        return indice

    def find_id_grafico_relacoes(x,y,mp):
        df = pd.read_csv("./csv/lista_relacoes.csv")
   
        X = [x]
        Y = [y]

        if mp == 't-SNE':
            indice = df[(df['x_tsne'].isin(X)) & (df['y_tsne'].isin(Y))].index

        else: 
            indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index

        return indice

    def find_id_grafico_entidades(x,y,mp):
        df = pd.read_csv("./csv/lista_entidades.csv")

        X = [x]
        Y = [y]

        if mp == 't-SNE':
            indice_aux = df[(df['x_tsne'].isin(X)) & (df['y_tsne'].isin(Y))].index

        else: 
            indice_aux = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index

        id_dodf_rel = df.id_dodf_rel[indice_aux]
        print(type(id_dodf_rel))
        print(id_dodf_rel)
        print(list(id_dodf_rel)[0])

        indice = find_id_tabela(list(id_dodf_rel)[0])

        return indice 

    def busca_lista_anotacoes(id_geral):

        df = pd.read_csv("./csv/lista_entidades.csv")
        id_geral = int(id_geral)

        #como resolvi o bug que tinha aqui: os tipos eram diferentes, então converti id_geral para int    
        indice = df[(df['id_geral'] == id_geral)].index
        info = []
        tipo_ent = df['tipo_ent'][indice]
        texto_ent = df['texto'][indice]
        info.append(list(tipo_ent)[0])
        info.append(list(texto_ent)[0])

        return info

    def update_contents(indice, df):
        contents = []

        tipo_rel = df.tipo_rel[indice]
        texto = df.texto[indice]
        idd = df['id_dodf_rel'][indice]
        anotacoes = list(df.anotacoes[indice])[0]
        list_anotacoes = literal_eval(anotacoes) 
        contents.append(html.H4("Ato",style={'text-align': 'center'}))
        contents.append(html.H5("Tipo:"))
        contents.append(html.P(tipo_rel,className="card-tab"))
        contents.append(html.H5("Texto:"))
        contents.append(html.P(texto,className="card-tab"))
        contents.append(html.H5("Id da relação:"))
        contents.append(html.P(idd,className="card-tab"))
        contents.append(html.H4("Entidades",style={'text-align': 'center'}))

        j = 0
        while j < len(list_anotacoes): 
            id_anno = list_anotacoes[j]
            info = busca_lista_anotacoes(id_anno)
            tipo_ent = info[0]
            texto_ent = info[1]
            contents.append(html.Div(className="card-tab",style={'align-items': 'center', 'justify-content':'center'}, children=[
                dcc.Dropdown(id=id_anno+'tipo_ent',
                                searchable=True,
                                clearable=False,
                                options=options_entidades,
                                placeholder="Select a label",
                                value=tipo_ent,),
                dcc.Textarea(id=id_anno, value=str(texto_ent),style={'width':'100%','min-height': '80px'}),
                html.Button(children=["Atualizar"], className="Button", id=id_anno+"buttonAtualizar", n_clicks=0),
                html.Button(children=["Confirmar"], className="Button", id=id_anno+"buttonConfirmar", n_clicks=0),
                html.Button(children=["Apagar"], className="Button", id=id_anno+"buttonApagar", n_clicks=0),
            ]))
            j += 1
        
        contents.append(html.Button(children=["CONFIRMAR TODOS"], className="Button", id=str(idd), n_clicks=0),)

        return contents
            
    @app.callback(
        [
            Output("selected-point", "children"),
        ],
        [
            Input("graph-3d-plot-tsne", "clickData"),
            Input("graph-entidades", "clickData"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input('datatable_relacoes', "derived_virtual_selected_rows"),
            Input('datatable_entidades', "derived_virtual_selected_rows")
        ],
        [
            State("dropdown-method", "value"),
            State('datatable_relacoes', "data"),
            State('datatable_entidades', "data"),
        ]
    )
    def explore_data(clickData,click_entidades,enviar, row_id_relacoes, row_id_entidades, mp, table_relacoes, table_entidades):
        df = pd.read_csv("./csv/lista_relacoes.csv")
        contents = []

        contents.append(html.H5("Clique em um ponto no layout para obter mais informações."),)

        context = dash.callback_context

        trigger = context.triggered[0]['prop_id']

        if row_id_relacoes is None:
            row_id_relacoes = []

        if row_id_entidades is None:
            row_id_entidades = []

        if str(trigger) == 'graph-3d-plot-tsne.clickData':
            x = clickData["points"][0]['x']
            y = clickData["points"][0]['y']

            indice = find_id_grafico_relacoes(x,y,mp)
            contents = update_contents(indice, df)
        
        elif str(trigger) == 'graph-entidades.clickData':
            x = click_entidades["points"][0]['x']
            y = click_entidades["points"][0]['y']
            print('passei por graph-entidades')

            indice = find_id_grafico_entidades(x,y,mp)
            contents = update_contents(indice, df)

        elif str(trigger) == 'datatable_relacoes.derived_virtual_selected_rows' and row_id_relacoes != []:
            selected_rows=[table_relacoes[i] for i in  row_id_relacoes]
            id_dodf_rel = selected_rows[0]["id_dodf_rel"]

            indice = find_id_tabela(id_dodf_rel)
            contents = update_contents(indice, df)

        elif str(trigger) == 'datatable_entidades.derived_virtual_selected_rows' and row_id_entidades != []:
            selected_rows=[table_entidades[i] for i in row_id_entidades]
            id_dodf_rel = selected_rows[0]["id_dodf_rel"]

            indice = find_id_tabela(id_dodf_rel)
            contents = update_contents(indice, df)
            
        return [contents]

    '''

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
            df = pd.read_csv("lista_relacoes.csv")

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
            df = pd.read_csv("lista_relacoes.csv")

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
            

            df.to_csv("lista_relacoes.csv",index=False)

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
            df = pd.read_csv("lista_relacoes.csv")

            indice = achar_indice(clickData,mp)

            df.at[indice, 'estado'] = "Confirmado"

            df.to_csv("lista_relacoes.csv",index=False)

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
        df = pd.read_csv("lista_relacoes.csv")
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
        df = pd.read_csv("lista_relacoes.csv")

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

            df.to_csv("lista_relacoes.csv",index=False)

            return [1]

        
        
        #i = 0
        #qnt = 0
        #while i < len(df):
        #    if df["estado"][i] == "Confirmado":
        #        qnt += 1
        #    i += 1
        

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
            df = pd.read_csv("lista_relacoes.csv")
            dff = df
            csv_string = dff.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8," + \
                urllib.parse.quote(csv_string)
        return [csv_string]

    '''
    
