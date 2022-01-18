import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

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
