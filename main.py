from extraction import extraction_callbacks, organize_content, return_tables
from multidimensional_projection import projecao_multi
from export import export_callbacks

import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.exceptions import PreventUpdate

import pandas as pd
import plotly.express as px
import re

from urllib.parse import quote as urlquote
import urllib

from ast import literal_eval

pd.options.mode.chained_assignment = None  # default='warn'

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
        'confirmado': '#9EE09E',
        'corrigido': ' #72ccd8',
        'nao_confirmado': '#bbbbbb',
        'em_duvida': '#FDFD97',
        'deletar': '#FFFFFF',
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
                        
                        
                        
                        html.Button(children=["Revisar anotações ->"], className="Button", id="button-revisar-anotacoes", n_clicks=0, style={"display":"none"}),
                        html.Button(id="value-button-revisar-anotacoes", className="Button",n_clicks=0, style={"display":"none"}),
                        
                        html.Button(children=["Download anotações ->"], className="Button", id="button-output-anotacoes", n_clicks=0, style={"display":"none"}),
                        
                        html.Button(children=["<- Revisar anotações"], className="Button", id="button-voltar-revisar-anotacoes", n_clicks=0, style={"display":"none"}),
                        html.Button(children=["Importar novas anotações ->"], className="Button", id="button-voltar-input-anotacoes", n_clicks=0, style={"display":"none"}),
                        
                        #html.Button(children=["Corrigir entidades ->"], className="Button", id="corrigir-entidades-button", n_clicks=0, style={"display":"none"}),
                        ],         
                ),

                # Canto direito do Header
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

        # página de ajuda (ainda precisa ser editado)
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

        # página de importação de anotações
        html.Div(id = "pagina-input-anotacoes",children =[
            # local para a inserção dos arquivos XML
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
                    # permitir fazer o upload de mais de um documento
                    multiple=True
                ),
            ], className='card'),
            
            # local onde aparece as anotações que foram extraídas, com a opção de salvá-las em um arquivo CSV
            html.Div(id='output-data-upload')], className='row'),
        ]),

        # página de correção de anotações - nível tipo dos atos
        html.Div( 
            className="row background",  
            id="pagina-revisar-anotacoes",         
            style={
                       "display": "none",
                       "grid-template-columns": "400px auto 400px",
                       "height":"auto",
                       },
            children=[

                # Tabelas                
                html.Div(
                    #className="card-ato",
                    id="lista_atos",
                    className="control-tabs",
                    children=[                       
                        dcc.Tabs(id='tabs_left', value='atos', children=[
                            # guia referente às informações do ponto que foi clicado por último
                            dcc.Tab(
                                label='RELAÇÕES',
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
                        ])                          
                    ],
                ),
                
                #Representações Gráficas
                html.Div(
                    id="pagina-revisar-anotacoes-meio",
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
                                                        html.Button("confirmar vários",id="button-confirmar-varios-relacoes", className="Button",n_clicks=0),
                                                        html.Button(id="button-confirmar-varios-relacoes-result", className="Button",n_clicks=0,style={"display":"none"}),
                                                                                  
                                                    ]
                                                ),
                                            ],
                                        ),
                                            dcc.Graph(id="graph-relacoes")
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
                                                        html.Button("confirmar vários",id="button-confirmar-varios-entidades", className="Button",n_clicks=0),
                                                        html.Button(id="button-confirmar-varios-entidades-result", className="Button",n_clicks=0,style={"display":"none"}),
                                                                                  
                                                    ]
                                                ),
                                            ],
                                        ),
                                            dcc.Graph(id="graph-entidades")
                                        ]),
                                ]),
                        ]),
                ]),
                
                # Painel de Controle
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
                                        html.Button(children=["ATUALIZAR ENTIDADES"], className="Button-control", id='flag-update-entidade-control',n_clicks=0, style={'display':'none'}),
                                        html.Button(children=["CONFIRMAR TODOS"], className="Button-control", id='confirmar-relacao-control',n_clicks=0, style={'display':'none'}),
                                        html.Button(children=["DELETAR RELAÇÃO"], className="Button-control", id='deletar-relacao-control', n_clicks=0, style={'display':'none'}),
                                        html.Button(id="flag-update-relacao-control", className="Button",n_clicks=0,style={"display":"none"}),
                                        html.Button(id="update-entidade", className="Button",n_clicks=0,style={"display":"none"}),
                                        html.Div(children=['id_anno','nada'],id="id_geral_entidade", style={'display':'none'}),
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
        html.Div(id = "pagina-output-anotacoes",children =[
            #Onde aparecem várias tabelas, uma para cada tipo de ato, com as entidades que foram extraídas
            dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="circle",
                ),
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
            Output("button-revisar-anotacoes", "style"),   
            Output("button-output-anotacoes", "style"), 
            Output("button-voltar-revisar-anotacoes", "style"), 
            Output("button-voltar-input-anotacoes", "style"), 

            Output("pagina-input-anotacoes", "style"),
            Output("pagina-revisar-anotacoes", "style"),
            Output("pagina-output-anotacoes", "style"),           
        ],
        [
            Input('upload-data', 'contents'),
            Input("button-revisar-anotacoes", "n_clicks"),   
            Input("button-output-anotacoes", "n_clicks"), 
            Input("button-voltar-revisar-anotacoes", "n_clicks"), 
            Input("button-voltar-input-anotacoes", "n_clicks"),
        ]
    )
    def control_displays(upload_data,revisar_anotacoes, output_anotacoes,voltar_revisar_anotacoes, voltar_input_anotacoes):       
        # vê qual foi o input que ativou o callback
        context = dash.callback_context
        trigger = context.triggered[0]['prop_id']

        displays = [
            {"display":"none"}, #button-revisar-anotacoes
            {"display":"none"}, #button-output-anotacoes
            {"display":"none"}, #button-voltar-revisar-anotacoes
            {"display":"none"}, #button-voltar-input-anotacoes

            {}, #pagina-input-anotacoes
            {"display":"none"}, #pagina-revisar-anotacoes
            {"display":"none"}, #pagina-output-anotacoes
        ]

        if str(trigger) == 'upload-data.contents':
            displays = [
                {}, #button-revisar-anotacoes
                {"display":"none"}, #button-output-anotacoes
                {"display":"none"}, #button-voltar-revisar-anotacoes
                {"display":"none"}, #button-voltar-input-anotacoes

                {}, #pagina-input-anotacoes
                {"display":"none"}, #pagina-revisar-anotacoes
                {"display":"none"}, #pagina-output-anotacoes
            ]

        elif str(trigger) == 'button-revisar-anotacoes.n_clicks':
            displays = [
                {"display":"none"}, #button-revisar-anotacoes
                {}, #button-output-anotacoes
                {"display":"none"}, #button-voltar-revisar-anotacoes
                {"display":"none"}, #button-voltar-input-anotacoes

                {"display":"none"}, #pagina-input-anotacoes
                {},#{"padding-left": "15px","padding-rigth": "15px","display": "grid","grid-template-columns": "400px auto 400px"}, #,"height": "100vh"pagina-revisar-anotacoes
                {"display":"none"}, #pagina-output-anotacoes
            ]

        elif str(trigger) == 'button-output-anotacoes.n_clicks':
            displays = [
                {"display":"none"}, #button-revisar-anotacoes
                {"display":"none"}, #button-output-anotacoes
                {}, #button-voltar-revisar-anotacoes
                {}, #button-voltar-input-anotacoes

                {"display":"none"}, #pagina-input-anotacoes
                {"display":"none"}, #pagina-revisar-anotacoes
                {}, #pagina-output-anotacoes
            ]

        elif str(trigger) == 'button-voltar-revisar-anotacoes.n_clicks':
            displays = [
                {"display":"none"}, #button-revisar-anotacoes
                {}, #button-output-anotacoes
                {"display":"none"}, #button-voltar-revisar-anotacoes
                {"display":"none"}, #button-voltar-input-anotacoes

                {"display":"none"}, #pagina-input-anotacoes
                {},#{"padding-left": "15px","padding-rigth": "15px","display": "grid","grid-template-columns": "400px auto 400px"}, #,"height": "100vh"pagina-revisar-anotacoes
                {"display":"none"}, #pagina-output-anotacoes
            ]

        elif str(trigger) == 'button-voltar-input-anotacoes.n_clicks':
            displays = [
                {"display":"none"}, #button-revisar-anotacoes
                {"display":"none"}, #button-output-anotacoes
                {"display":"none"}, #button-voltar-revisar-anotacoes
                {"display":"none"}, #button-voltar-input-anotacoes

                {}, #pagina-input-anotacoes
                {"display":"none"}, #pagina-revisar-anotacoes
                {"display":"none"}, #pagina-output-anotacoes
            ]

        else: 
            displays = [
            {"display":"none"}, #button-revisar-anotacoes
            {"display":"none"}, #button-output-anotacoes
            {"display":"none"}, #button-voltar-revisar-anotacoes
            {"display":"none"}, #button-voltar-input-anotacoes

            {}, #pagina-input-anotacoes
            {"display":"none"}, #pagina-revisar-anotacoes
            {"display":"none"}, #pagina-output-anotacoes
        ]

        return displays
    
    # Parte 1 - Extração de anotações do XML
    extraction_callbacks(app)

    export_callbacks(app)
    
    '''
    @app.callback(
        [
            Output('output-anotacoes-revisadas', 'children'),
        ],
        [
            Input("button-output-anotacoes", "n_clicks"),
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
            Output("value-button-revisar-anotacoes", "n_clicks"),
        ],
        [
            Input("button-revisar-anotacoes", "n_clicks")
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
                figure = px.scatter(dict_dfs, x=X, y=Y,hover_name='texto', color = 'tipo_ent',color_discrete_sequence=px.colors.qualitative.Pastel)
            else:
                figure = px.scatter(dict_dfs, x=X, y=Y,hover_name='texto', color = 'estado_ent',color_discrete_map=colors)
                    
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
            Input("value-button-revisar-anotacoes", "n_clicks"),
            Input('flag-update-relacao-control', 'n_clicks'),
        ]
    )
    def montar_tabela_relacoes(tipos,run,flag_relacoes):
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

        temp = df2.estado_rel
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
            Input("value-button-revisar-anotacoes", "n_clicks"),
            Input('flag-update-relacao-control', 'n_clicks'),
            Input('flag-update-entidade-control', 'n_clicks'),
        ]
    )
    def montar_tabela_entidades(tipos,run,flag_relacoes,flag_entidades):
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
            Output("graph-relacoes", "figure"),
            Output("flag-warning-atos", 'n_clicks'),
        ],
        [
            Input("dropdown-atos","value"),
            Input("value-button-revisar-anotacoes", "n_clicks"),
            Input("dropdown-method", "value"),
            Input("dropdown-label", "value"),
            Input("confirmar-classe-button-result", "n_clicks"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input("button-confirmar-varios-relacoes-result", "n_clicks"),
            Input('flag-update-relacao-control', 'n_clicks'),
        ]    
    )
    def display_grafico_relacoes(tipos,run,mp,label,confirmar,enviar,confirmar_varios,flag):
        display = 0
        if run == 0:
            df = pd.read_csv("./csv/relacoes_temp.csv")
            figure = generate_figure(df,'TEMP',label,'rel')
            return [figure,display]
        else: #if run > 0 or confirmar > 0 or enviar > 0 or confirmar_varios > 0:
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
            Input("value-button-revisar-anotacoes", "n_clicks"),
            Input("dropdown-method-entidades", "value"),
            Input("dropdown-label-entidades", "value"),
            Input("confirmar-classe-button-result", "n_clicks"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input("button-confirmar-varios-entidades-result", "n_clicks"),
            Input('flag-update-relacao-control', 'n_clicks'),
            Input('flag-update-entidade-control', 'n_clicks'),
        ]    
    )
    def display_grafico_entidades(tipos,run,mp,label,confirmar,enviar,confirmar_varios,flag_relacoes,flag_entidades):
        if run == 0:
            df = pd.read_csv("./csv/entidades_temp.csv")
            figure = generate_figure(df,'TEMP','estado','ent')
        else: #if run > 0 or confirmar > 0 or enviar > 0 or confirmar_varios > 0:
            df = pd.read_csv("./csv/lista_entidades.csv")
            
            df2 = df
            if "Todos" not in tipos:
                df2 = df[(df.tipo_rel == tipos[0])]
                if len(df2) == 0:
                    
                    raise PreventUpdate
                    figure = generate_figure(df,mp,label,'ent')
                    return [figure]
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
        estado_ent = df['estado_ent'][indice]
        print(id_geral)
        print(indice)
        print(list(tipo_ent))
        print(tipo_ent)
        info.append(list(tipo_ent)[0])
        info.append(list(texto_ent)[0])
        info.append(list(estado_ent)[0])

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
            estado_ent = info[2]
            dict_color_buttons_entidade = {'corrigir':'#bbbbbb','confirmar':'#bbbbbb','em_duvida':'#bbbbbb','deletar':'#bbbbbb'}

            if estado_ent == "confirmado":
                dict_color_buttons_entidade['confirmar'] = '#72ccd8'
            elif estado_ent == "corrigido":
                dict_color_buttons_entidade['corrigir'] = '#72ccd8'
            elif estado_ent == "em_duvida":
                dict_color_buttons_entidade['em_duvida'] = '#72ccd8'
            elif estado_ent == "deletar":
                dict_color_buttons_entidade['deletar'] = '#72ccd8'


            contents.append(html.Div(className="card-tab",style={'align-items': 'center', 'justify-content':'center'}, children=[
                dcc.Dropdown(id={'type': 'tipo_ent','index': id_anno},
                                searchable=True,
                                clearable=False,
                                options=options_entidades,
                                placeholder="Select a label",
                                value=tipo_ent,),
                dcc.Textarea(id={'type': 'text_ent','index': id_anno}, value=str(texto_ent),style={'width':'100%','min-height': '80px'}),
                
                html.Button(children=["confirmar"], className="Button-control", id={'type': 'confirmar-entidade','index': id_anno}, n_clicks=0,value=id_anno,style={'background': dict_color_buttons_entidade['confirmar']}),
                html.Button(children=["corrigir"], className="Button-control", id={'type': 'corrigir-entidade','index': id_anno}, n_clicks=0,value=id_anno,style={'background': dict_color_buttons_entidade['corrigir']}),
                html.Button(children=["em duvida"], className="Button-control", id={'type': 'duvida-entidade','index': id_anno}, n_clicks=0,value=id_anno,style={'background': dict_color_buttons_entidade['em_duvida']}),
                html.Button(children=["deletar"], className="Button-control", id={'type': 'deletar-entidade','index': id_anno}, n_clicks=0,value=id_anno,style={'background': dict_color_buttons_entidade['deletar']}),
                html.Div(children=[id_anno,'nada','n'],id={'type': 'id_geral','index': id_anno}, style={'display':'none'})
                
            ]))
            j += 1
        
        """contents.append(html.Button(children=["CONFIRMAR TODOS"], className="Button-control", id={'type': 'confirmar-relacao','index': list(idd)[0]},n_clicks=0,value=list(idd)[0]),)
        contents.append(html.Button(children=["DELETAR RELAÇÃO"], className="Button-control", id={'type': 'deletar-relacao','index': list(idd)[0]}, n_clicks=0,value=list(idd)[0]),)
        html.Div(id={'type': 'flag-update-relacao-control','index': list(idd)[0]})
        """
        

        return contents
            
    @app.callback(
        [
            Output("selected-point", "children"),
            Output("flag-update-entidade-control", "style"),
            Output("confirmar-relacao-control", "style"),
            Output("deletar-relacao-control", "style"),
            Output("confirmar-relacao-control", "value"),
            Output("deletar-relacao-control", "value"),
        ],
        [
            Input("graph-relacoes", "clickData"),
            Input("graph-entidades", "clickData"),
            Input("enviar-corrigir-classe-button-result", "n_clicks"),
            Input('datatable_relacoes', "derived_virtual_selected_rows"),
            Input('datatable_entidades', "derived_virtual_selected_rows"),
            
        ],
        [
            State("dropdown-method", "value"),
            State('datatable_relacoes', "data"),
            State('datatable_entidades', "data")
        ]
    )
    def explore_data(clickData,click_entidades,enviar, row_id_relacoes, row_id_entidades, mp, table_relacoes, table_entidades):
        
        df = pd.read_csv("./csv/lista_relacoes.csv")
        contents = []
        style_atualizar = {'display':'none'}
        style_confirmar = {'display':'none'}
        style_deletar = {'display':'none'}
        value = ''

        contents.append(html.H5("Clique em um ponto no layout para obter mais informações."),)

        context = dash.callback_context
        trigger = context.triggered[0]['prop_id']

        if row_id_relacoes is None:
            row_id_relacoes = []

        if row_id_entidades is None:
            row_id_entidades = []

        if str(trigger) == 'graph-relacoes.clickData':
            x = clickData["points"][0]['x']
            y = clickData["points"][0]['y']

            indice = find_id_grafico_relacoes(x,y,mp)
            contents = update_contents(indice, df)
            style_atualizar = {}
            style_confirmar = {}
            style_deletar = {}
            value = str(indice[0])
        
        elif str(trigger) == 'graph-entidades.clickData':
            x = click_entidades["points"][0]['x']
            y = click_entidades["points"][0]['y']

            indice = find_id_grafico_entidades(x,y,mp)
            contents = update_contents(indice, df)
            style_atualizar = {}
            style_confirmar = {}
            style_deletar = {}
            value = str(indice[0])

        elif str(trigger) == 'datatable_relacoes.derived_virtual_selected_rows' and row_id_relacoes != []:
            selected_rows=[table_relacoes[i] for i in  row_id_relacoes]
            id_dodf_rel = selected_rows[0]["id_dodf_rel"]

            indice = find_id_tabela(id_dodf_rel)
            contents = update_contents(indice, df)
            style_atualizar = {}
            style_confirmar = {}
            style_deletar = {}
            value = str(indice[0])

        elif str(trigger) == 'datatable_entidades.derived_virtual_selected_rows' and row_id_entidades != []:
            selected_rows=[table_entidades[i] for i in row_id_entidades]
            id_dodf_rel = selected_rows[0]["id_dodf_rel"]

            indice = find_id_tabela(id_dodf_rel)
            contents = update_contents(indice, df)
            style_atualizar = {}
            style_confirmar = {}
            style_deletar = {}
            value = str(indice[0])
            
        return [contents, style_atualizar, style_confirmar, style_deletar, value,value]


    # CONFIRMANDO E DELETANDO TODAS AS ANOTACOES DE UMA RELACAO

    def update_entidade_relacao(id_geral, estado):
        df = pd.read_csv("./csv/lista_entidades.csv")
        id_geral = int(id_geral)    
        indice = df[(df['id_geral'] == id_geral)].index
        estado_ent = list(df.estado_ent[indice])[0]
        if estado == 'deletar':
            df.estado_ent[indice] = estado
        elif estado_ent == 'nao_confirmado':
            df.estado_ent[indice] = estado
        
        df.to_csv("./csv/lista_entidades.csv", index=False)

    def update_relacao_simples(indice,estado):
        df = pd.read_csv("./csv/lista_relacoes.csv")
        anotacoes = df.anotacoes[indice]
        list_anotacoes = literal_eval(anotacoes) 

        j = 0
        while j < len(list_anotacoes): 
            id_anno = list_anotacoes[j]
            update_entidade_relacao(id_anno,estado)
            j += 1

        df.estado_rel[indice] = estado
        df.to_csv("./csv/lista_relacoes.csv", index=False)

    def update_relacao_avancado(indice):
        df = pd.read_csv("./csv/lista_relacoes.csv")
        anotacoes = df.anotacoes[indice]
        list_anotacoes = literal_eval(anotacoes) 
        estados_ent = []
        estado = df.estado_rel[indice]

        j = 0
        all_confirmado = 1
        all_deletar = 1
        while j < len(list_anotacoes): 
            id_anno = list_anotacoes[j]
            info = busca_lista_anotacoes(id_anno)
            if info[2] == 'nao_confirmado':
                all_confirmado = 0
            if info[2] != 'deletar':
                all_deletar = 0
            estados_ent.append(info[2])
            j += 1

        if 'em_duvida' in estados_ent:
            estado = 'em_duvida'

        elif 'corrigido' in estados_ent:
            estado = 'corrigido'

        elif all_confirmado:
            estado = 'confirmado'

        elif all_deletar:
            estado = 'deletar'

        df.estado_rel[indice] = estado
        df.to_csv("./csv/lista_relacoes.csv", index=False)

    @app.callback(
        [
            Output('flag-update-relacao-control', 'n_clicks'),
        ],
        [
            Input("confirmar-relacao-control", "n_clicks"),
            Input("deletar-relacao-control", "n_clicks"),
            Input('flag-update-entidade-control', 'n_clicks')
        ],
        [
            State("confirmar-relacao-control", "value")
        ]
    )
    def update_relacao_control(n1,n2,flag_entidades,indice):
        context = dash.callback_context
        trigger = context.triggered[0]['prop_id']

        if str(trigger) == 'confirmar-relacao-control.n_clicks':
            update_relacao_simples(int(indice),'confirmado')
        
        elif str(trigger) == 'deletar-relacao-control.n_clicks':
            update_relacao_simples(int(indice),'deletar')

        elif str(trigger) == 'flag-update-entidade-control.n_clicks':
            update_relacao_avancado(int(indice))


        return [n1+n2]


    #CONFIRMANDO VÁRIAS RELACOES AO MESMO TEMPO

    def update_relacao_simples2(indice,estado):
        df = pd.read_csv("./csv/lista_relacoes.csv")
        anotacoes = list(df.anotacoes[indice])
        
        if len(anotacoes) == 0:
            update_apenas_relacao(indice,'em_duvida')

        else: 
            anotacoes = list(df.anotacoes[indice])[0]
            list_anotacoes = literal_eval(anotacoes) 

            j = 0
            while j < len(list_anotacoes): 
                id_anno = list_anotacoes[j]
                update_entidade(id_anno,estado)
                j += 1

            df.estado_rel[indice] = estado
            df.to_csv("./csv/lista_relacoes.csv", index=False)

    def update_apenas_relacao(indice,estado):
        df = pd.read_csv("./csv/lista_relacoes.csv")
        df.estado_rel[indice] = estado
        df.to_csv("./csv/lista_relacoes.csv", index=False)


    @app.callback(
        [
            Output("button-confirmar-varios-relacoes-result", "n_clicks")
        ],
        [
            Input("button-confirmar-varios-relacoes", "n_clicks"),
        ],
        [
            State("graph-relacoes", "selectedData"),
            State("dropdown-method", "value")
        ]
    )
    def confirmar_varios_relacoes(confirmar, selectedData, mp):

        if selectedData:  
            j = 0
            for point in selectedData["points"]:
                x = selectedData["points"][j]['x']
                y = selectedData["points"][j]['y']

                indice = find_id_grafico_relacoes(x,y,mp)
                update_relacao_simples2(indice,'confirmado')
                j += 1

            return [1]
        return [0]

    #CONFIRMANDO VÁRIAS ENTIDADES AO MESMO TEMPO

    def update_entidade2(id_geral, estado):
        df = pd.read_csv("./csv/lista_entidades.csv")
        id_geral = int(id_geral)    
        indice = df[(df['id_geral'] == id_geral)].index
        estado_ent = list(df.estado_ent[indice])[0]
        print(estado)
        if estado_ent == 'nao_confirmado':
            df.estado_ent[indice] = estado
        
        df.to_csv("./csv/lista_entidades.csv", index=False)

    @app.callback(
        [
            Output("button-confirmar-varios-entidades-result", "n_clicks")
        ],
        [
            Input("button-confirmar-varios-entidades", "n_clicks"),
        ],
        [
            State("graph-entidades", "selectedData"),
            State("dropdown-method-entidades", "value")
        ]
    )
    def confirmar_varios_entidades(confirmar, selectedData, mp):
        if selectedData:  
            df = pd.read_csv("./csv/lista_entidades.csv")
            j = 0
            for point in selectedData["points"]:
                x = selectedData["points"][j]['x']
                y = selectedData["points"][j]['y'] 

                X = [x]
                Y = [y]

                if mp == 't-SNE':
                    indice = df[(df['x_tsne'].isin(X)) & (df['y_tsne'].isin(Y))].index

                else: 
                    indice = df[(df['x_umap'].isin(X)) & (df['y_umap'].isin(Y))].index

                id_geral = list(df.id_geral[indice])[0] 
                update_entidade2(id_geral,'confirmado')
                j += 1

            return [1]
        return [0]
        
    def update_entidade(id_geral, estado):
        df = pd.read_csv("./csv/lista_entidades.csv")
        id_geral = int(id_geral)    
        indice = df[(df['id_geral'] == id_geral)].index
        df.estado_ent[indice] = estado
        df.to_csv("./csv/lista_entidades.csv", index=False)

    #ATUALIZANDO APENAS UMA ENTIDADE

    @app.callback(
        [
            Output({"index": MATCH, "type": "id_geral"}, "children"),    
        ],
        [
            Input({"index": MATCH, "type": "confirmar-entidade"}, "n_clicks"),
            Input({"index": MATCH, "type": "corrigir-entidade"}, "n_clicks"),
            Input({"index": MATCH, "type": "duvida-entidade"}, "n_clicks"),
            Input({"index": MATCH, "type": "deletar-entidade"}, "n_clicks")
        ],
        [
            State({"index": MATCH, "type": "id_geral"}, "children")
        ]
    )
    def trigger_entidade(confirmar,corrigir,duvida,deletar,children): 

        if deletar is None:
            raise PreventUpdate
        comando = children
        context = dash.callback_context
        trigger = context.triggered[0]['prop_id']
        id_geral = children[0]


        if trigger == '{"index":"'+str(id_geral)+'","type":"confirmar-entidade"}.n_clicks':
            comando[1] ='confirmado'
            comando[2] ='s'

        elif trigger == '{"index":"'+str(id_geral)+'","type":"corrigir-entidade"}.n_clicks':
            comando[1] ='corrigir'
            comando[2] ='s'
        
        elif trigger == '{"index":"'+str(id_geral)+'","type":"duvida-entidade"}.n_clicks':
            comando[1] ='em_duvida'
            comando[2] ='s'

        elif trigger == '{"index":"'+str(id_geral)+'","type":"deletar-entidade"}.n_clicks':
            comando[1] ='deletar'
            comando[2] ='s'

        return [comando]

    def corrigir_entidade(id_geral,tipo,texto):
        df = pd.read_csv("./csv/lista_entidades.csv")
            
        id_geral = int(id_geral)    
        indice = df[(df['id_geral'] == id_geral)].index
        df.tipo_ent[indice] = tipo
        df.texto[indice] = texto
        df.estado_ent[indice] = 'corrigido'

        df.to_csv("./csv/lista_entidades.csv", index=False)

    @app.callback(
        [
            Output('update-entidade', 'n_clicks'),
        ],
        [
            Input({"index": ALL, "type": "id_geral"}, "children") 
        ],
        [
            State('flag-update-entidade-control', 'n_clicks'),
            State({"index": ALL, "type": "tipo_ent"}, "value"),
            State({"index": ALL, "type": "text_ent"}, "value")
        ]
    )
    def update_entidade_control(values,clicks,tipos,textos):

        trigger = []
        if values != []:
            for i in range(len(values)):
                if values[i][2] == 's':
                    trigger = values[i]
                    id_geral = trigger[0]
                    do = trigger[1]
                    if do == 'corrigir':

                        corrigir_entidade(id_geral,tipos[i],textos[i])
                    else:
                        update_entidade(id_geral, do)
            if trigger == []:
                raise PreventUpdate

            return [clicks+1]
        return [clicks]