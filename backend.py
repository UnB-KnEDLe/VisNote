import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd 
import plotly.express as px
import urllib

data_dict = {
    "DODF2D": pd.read_csv('./csv/dodf.csv'),
    "Aposentadoria": {"DODF_Aposentadoria2D": pd.read_csv('./csv/aposentadorias.csv'),
                      "DODF_Aposentadoria2018": pd.read_csv('./csv/aposentadorias_2018.csv'),
                      "DODF_Aposentadoria2019": pd.read_csv('./csv/aposentadorias_2019.csv'), },
    "Editais": {"DODF_Editais2D": pd.read_csv('./csv/editais.csv'),
                "DODF_Editais2013": pd.read_csv('./csv/editais_2013.csv'),
                "DODF_Editais2014": pd.read_csv('./csv/editais_2014.csv'),
                "DODF_Editais2015": pd.read_csv('./csv/editais_2015.csv'),
                "DODF_Editais2016": pd.read_csv('./csv/editais_2016.csv'),
                "DODF_Editais2017": pd.read_csv('./csv/editais_2017.csv'),
                "DODF_Editais2018": pd.read_csv('./csv/editais_2018.csv'),
                "DODF_Editais2019": pd.read_csv('./csv/editais_2019.csv'),
                "DODF_Editais2020": pd.read_csv('./csv/editais_2020.csv'),
                "DODF_Editaisoutros": pd.read_csv('./csv/editais_outros.csv')
                },
    "Exoneracoes": {"DODF_Exoneracoes2D": pd.read_csv('./csv/exoneracoes.csv'),
                    "DODF_Exoneracoes2010": pd.read_csv('./csv/exoneracoes_2010.csv'),
                    "DODF_Exoneracoes2011": pd.read_csv('./csv/exoneracoes_2011.csv'),
                    "DODF_Exoneracoes2012": pd.read_csv('./csv/exoneracoes_2012.csv'),
                    "DODF_Exoneracoes2013": pd.read_csv('./csv/exoneracoes_2013.csv'),
                    "DODF_Exoneracoes2014": pd.read_csv('./csv/exoneracoes_2014.csv'),
                    "DODF_Exoneracoes2015": pd.read_csv('./csv/exoneracoes_2015.csv'),
                    "DODF_Exoneracoes2016": pd.read_csv('./csv/exoneracoes_2016.csv'),
                    "DODF_Exoneracoes2017": pd.read_csv('./csv/exoneracoes_2017.csv'),
                    "DODF_Exoneracoes2018": pd.read_csv('./csv/exoneracoes_2018.csv'),
                    "DODF_Exoneracoes2019": pd.read_csv('./csv/exoneracoes_2019.csv'),
                    "DODF_Exoneracoes2020": pd.read_csv('./csv/exoneracoes_2020.csv'),
                    },
}

DODF = pd.read_csv('./csv/dodf.csv')
global dfAnno
dfAnno = pd.DataFrame(DODF)


def create_layout(app):
    # Actual layout of the app
    return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            # Header
            html.Div(
                className="row header",
                id="app-header",
                style={"background-color": "#1F2132"},
                children=[
                    html.Img(
                        src=app.get_asset_url("knedle-logo4.png"),
                        className="logo",
                        id="logo",
                    ),
                    html.Div(
                        style={"display": "flex"},
                        children=[
                            html.Button(
                                "About Us",
                                id="about-button"
                            ),
                            html.H3(
                                "VisNote",
                                id="app-title",
                            ),
                        ]
                    ),
                ]),

            # About Us
            html.Div(
                className="row background",
                id="about-us",
                children=[
                    html.Div(
                        id="about-content",
                        children=[
                            html.H4(id="about-title",
                                    style={"text-align": "center"},
                                    children=["About Us"],
                                    ),
                            html.Div(id="about-text",
                                     children=[
                                        html.H6(
                                            "The scatter plot below is the result of running the t-SNE algorithm on DODF's datasets, resulting in 2D and 3D visualizations of the documents."),
                                        html.H6("Official publications such as the Diario Oficial do Distrito Federal (DODF) are sources of information on all official government acts. Although these documents are rich in knowledge, analysing these texts manually by specialists is a complex and unfeasible task considering the growing volume of documents, the result of the frequent number of publications in the Distrito Federal Government's (GDF) communication vehicle."),
                                        html.H6("VisNote aims to facilitate the visualization of such information using unsupervised machine learning methods and data visualization techniques. This is one of the tools developed by the KnEDLe Project. To learn more about us, click on 'Learn More' below.")
                                     ]),
                            html.Br(),
                            html.Button(children=[
                                html.A("Learn More", href='https://unb-knedle.github.io/', target="_blank", id="learn-more-button")], className="Button0"),
                        ]),
                    html.Hr(),
                ],
            ),

            # Help
            html.Div(
                className="row background",
                id="help",
                style={"display": "none"},
                children=[
                    html.H4(id="help-title",
                            style={"text-align": "center"},
                            children=["How to use DODF Annotator"],
                            ),
                    html.Div(id="help-text",
                             children=[
                                html.H5("1. Add new label."),
                                html.H6("[escrever]"),
                                html.H5("2. Select a set of points."),
                                html.H6("[escrever]"),
                                html.H5("3. Annotate selected points."),
                                html.H6("               [escrever]"),
                                html.H5("4. Unlabel."),
                                html.H6("               [escrever]"),
                                html.H5("5. Navigate through the points."),
                                html.H6("               [escrever]"),
                                html.H5(
                                    "       5.1 Getting more information about them."),
                                html.H6("               [escrever]"),
                                html.H5("       5.1 Zooming."),
                                html.H6("           [escrever]"),
                                html.H5(
                                    "       5.2 Visualizing only one specific label."),
                                html.H6("               [escrever]"),
                                html.H5("6. Download annotations."),
                                html.H6("       [escrever]"),
                             ]),
                    html.Br(),
                    html.Button(children=[
                        html.A("Tutorial Video", href='https://unb-knedle.github.io/', target="_blank", id="tutorial-button")], className="Button0"),
                    html.Hr(),
                ],
            ),

            # Homepage
            html.Div(
                className="row background",
                id="homepage",
                style={"padding": "15px",
                       "display": "grid",
                       "grid-template-columns": "auto 400px",
                       "height": "100vh"
                       },
                children=[
                    html.Div(
                        style={"height": "100%"},
                        children=[
                            # menu com os controles
                            html.Div(
                                className="row background",
                                id="menu",
                                children=[
                                    # controle/botões/menu da página de exploração
                                    html.Div(
                                        id="explore-data",
                                        style={"display": "grid",
                                               "grid-template-columns": "70% 30%",
                                               },
                                        children=[
                                            # controles referentes ao conjunto de dados
                                            html.Div(
                                                style={"display": "grid",
                                                       "grid-template-columns": "50% 50%",
                                                       },
                                                children=[
                                                    # seleção do dataset
                                                    html.Div(
                                                        style={
                                                            "display": "grid", "grid-template-columns": "minmax(130px, auto) 27vh"},
                                                        children=[
                                                            html.Label(
                                                                style={
                                                                    "display": "grid",
                                                                    "place-items": "center start"
                                                                },
                                                                children=[
                                                                    "Select a Dataset: "]
                                                            ),
                                                            dcc.Dropdown(
                                                                id="dropdown-dataset",
                                                                searchable=False,
                                                                clearable=False,
                                                                options=[
                                                                    {
                                                                        "label": "DODF",
                                                                        "value": "DODF",
                                                                    },
                                                                    {
                                                                        "label": "DODF - Aposentadoria",
                                                                        "value": "DODF_Aposentadoria",
                                                                    },
                                                                    {
                                                                        "label": "DODF - Editais",
                                                                        "value": "DODF_Editais",
                                                                    },
                                                                    {
                                                                        "label": "DODF - Exoneracoes",
                                                                        "value": "DODF_Exoneracoes",
                                                                    },
                                                                ],
                                                                placeholder="Select a dataset",
                                                                value="DODF",
                                                            )
                                                        ]),
                                                    # seleção do ano do dataset, caso tenha essa opção
                                                    html.Div(
                                                        id="segmentos-controls",
                                                        style={
                                                            "display": "none", "grid-template-columns": "auto auto"},
                                                        children=[
                                                            html.Label(
                                                                style={"display": "grid", "place-items": "center"}, children=["Select a year: "]),
                                                            dcc.Dropdown(
                                                                id="dropdown-segmentos",
                                                                searchable=False,
                                                                clearable=False,
                                                                options=[
                                                                    {
                                                                        "label": "Todos",
                                                                        "value": "todos",
                                                                    },
                                                                ],
                                                                placeholder="Select a year",
                                                                value="todos",
                                                            ),
                                                        ],
                                                    ),

                                                ],
                                                # botão que vai para a página de anotação
                                            ),
                                            html.Button(
                                                children=["Annotate ", html.I(className="fas fa-lg fa-pen-square")
                                                ], className="Button1", id="annotate-button", style={"float": "right"}, n_clicks=0),
                                        ]
                                    ),
                                    # controle/botões/menu da página de anotação
                                    html.Div(
                                        id="annotate-data",
                                        style={"display": "none", },
                                        children=[
                                            html.Div(style={"display": "grid", "grid-template-columns": "150px 150px 350px"}, children=[
                                                html.Button(
                                                    children=["Start"], className="Button2", id="start-button", n_clicks=0),
                                                dcc.Dropdown(
                                                    id="dropdown-label",
                                                    #style={"margin-left": "10px"},
                                                    searchable=False,
                                                    clearable=False,
                                                    options=[
                                                        {
                                                            "label": "- Unlabel",
                                                            "value": "Unlabeled",
                                                        },
                                                        {
                                                            "label": "+ Add label",
                                                            "value": "add_label",
                                                        },
                                                    ],
                                                    placeholder="Select a label",
                                                    value="add_label",
                                                ),
                                                html.Div(id="insert-new-label", style={"display": "none"}, children=[
                                                    "New Label: ",
                                                    dcc.Input(
                                                        id='input-new-label', value='(Insert new label)', type='text'),
                                                    html.Button(id='submit-button', className="Button3", n_clicks=0, children='Submit'), ],
                                                ),
                                            ]),

                                            html.Button(
                                                children=[html.I(className="fas fa-2x fa-question-circle")], className="Button5", id="help-button", n_clicks=0),
                                            html.Button(
                                                children=[html.I(className="fas fa-lg fa-download"), " Download"], className="Button4", id="finish-button", n_clicks=0),
                                        ]
                                    )
                                ],
                            ),
                            # gráfico/ aréa destinada às visualizações
                            dcc.Graph(
                                id="graph-3d-plot-tsne", style={"height": "90vh"})
                        ],
                    ),
                    # telas que mostram informações extras sob demanda
                    html.Div(
                        id="control-tabs",
                        children=[
                            dcc.Tabs(id='tabs', value='data', children=[
                                # guia referente a breve descrição do conjunto de dados presente no layout
                                dcc.Tab(
                                    label='Dataset',
                                    value='data',
                                    children=html.Div(className='control-tab', style={"padding": "20px",  "align-content": "center", "text-align": "center"}, children=[
                                        html.Div(id="dataset"),
                                    ]),
                                ),
                                # guia referente às informações do ponto que foi clicado por último
                                dcc.Tab(
                                    label='Selected point',
                                    value='point',
                                    children=html.Div(className='control-tab', style={"padding": "5px"}, children=[
                                        html.Div(id="selected-point"),
                                    ]),
                                ),
                            ])
                        ]
                    ),
                ],
            ),

            html.Div(id="qnt-annotations", children=[],
                     style={"display": "none"}),

            html.Div(id="download-page",
                     className="row background",
                     style={"display": "none",
                     "place-items": "center"},
                     children=[

                         html.Div(
                             id="control-download",
                             children=[
                                 html.A(
                                     html.Button(
                                         children=[html.I(className="fas fa-lg fa-download"),' Download CSV'], id="download-button", className="Button1", n_clicks=0),
                                     id='download-link',
                                     download="annotations_teste.csv",
                                     href="",
                                     target="_blank"
                                 ),
                                 html.Div(style={"display": "grid",
                                 "grid-template-columns": "auto auto",
                                 "gap": "15px"},
                                 children=[
                                     html.Button(children=[html.I(className="fas fa-lg fa-backward"), " Return to the previous annotation process."],
                                                 className="Button1", id="return-button", n_clicks=0),
                                     html.Button(children=[html.I(className="fas fa-lg fa-exchange-alt"), " Select a different data set to annotate."],
                                                 className="Button1", id="end-button", n_clicks=0),
                                 ])

                             ]
                         ),

                         # Download
                         html.Div(id='download',
                                  className='card-csv', children=[])





                     ],
                     )
        ],
    )


def demo_callbacks(app):
    def generate_figure_TSNE(df):
        figure = px.scatter(df, x='x', y='y', color='label',
                            color_discrete_sequence=px.colors.qualitative.Pastel)

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
            itemclick="toggleothers"
        ),
            margin=dict(l=40, r=40, t=50, b=40))

        return figure

    @app.callback(
        Output("dataset", "children"),
        [
            Input("dropdown-dataset", "value"),
        ],
    )
    def display_dataset(dataset):
        contents = []
        if dataset == 'DODF':
            contents.append(html.H3("DODF"))
            contents.append(
                html.P("Este conjunto de dados possui 717 instâncias."))
            contents.append(html.P(
                "Elas representam diferente tipos de atos retirados do DODF. Cada instância possui apenas um atributo, que é o conteúdo do ato."))
            contents.append(html.P(
                "Os pontos no gráfico ao lado representam as instâncias deste conjunto de dados."))

        elif dataset == 'DODF_Aposentadoria':
            contents.append(html.H3("DODF - Aposentadoria"))
            contents.append(
                html.P("Este conjunto de dados possui 5516 instâncias. "))
            contents.append(html.P(
                "Elas representam dados de atos de aposentadoria publicados no DODF em 2018 e 2019. Cada instância possui 17 atributos."))
            contents.append(html.P(
                "Os pontos no gráfico ao lado representam as instâncias deste conjunto de dados."))

        elif dataset == 'DODF_Editais':
            contents.append(html.H3("DODF - Editais"))
            contents.append(
                html.P("Este conjunto de dados possui 13872 instâncias."))
            contents.append(html.P(
                "Elas representam dados de editais que foram publicados no DODF entre os anos de 2013 e 2020. Cada instância possui 20 atributos."))
            contents.append(html.P(
                "Os pontos no gráfico ao lado representam as instâncias deste conjunto de dados."))

        elif dataset == 'DODF_Exoneracoes':
            contents.append(html.H3("DODF - Exoneracoes"))
            contents.append(
                html.P("Este conjunto de dados possui 45530 instâncias. "))
            contents.append(html.P(
                "Elas representam dados de atos de exoneração que foram publicados no DODF entre os anos de 2010 e 2020. Cada instância possui 15 atributos."))
            contents.append(html.P(
                "Os pontos no gráfico ao lado representam as instâncias deste conjunto de dados. "))

        return contents

    @app.callback(
        [
            Output("segmentos-controls", "style"),
            Output("dropdown-segmentos", "options"),
        ],
        [
            Input("dropdown-dataset", "value")
        ],
    )
    def display_segmentos(dataset):
        options = []
        if dataset != "DODF":
            if dataset == "DODF_Aposentadoria":
                options = [
                    {"label": "Todos", "value": "todos", },
                    {"label": "2018", "value": "2018", },
                    {"label": "2019", "value": "2019", }
                ]

            elif dataset == "DODF_Editais":
                options = [
                    {"label": "Todos", "value": "todos", },
                    {"label": "2013", "value": "2013", },
                    {"label": "2014", "value": "2014", },
                    {"label": "2015", "value": "2015", },
                    {"label": "2016", "value": "2016", },
                    {"label": "2017", "value": "2017", },
                    {"label": "2018", "value": "2018", },
                    {"label": "2019", "value": "2019", },
                    {"label": "2020", "value": "2020", },
                    {"label": "Ano não mencionado", "value": "outros", }
                ]

            elif dataset == "DODF_Exoneracoes":
                options = [
                    {"label": "Todos", "value": "todos", },
                    {"label": "2010", "value": "2010", },
                    {"label": "2011", "value": "2011", },
                    {"label": "2012", "value": "2012", },
                    {"label": "2013", "value": "2013", },
                    {"label": "2014", "value": "2014", },
                    {"label": "2015", "value": "2015", },
                    {"label": "2016", "value": "2016", },
                    {"label": "2017", "value": "2017", },
                    {"label": "2018", "value": "2018", },
                    {"label": "2019", "value": "2019", },
                    {"label": "2020", "value": "2020", },
                ]

            return {"display": "grid", "grid-template-columns": "150px 200px"}, options
        else:
            return {"display": "none"}, options

    @app.callback(
        Output("graph-3d-plot-tsne", "figure"),

        [
            Input("dropdown-dataset", "value"),
            Input("dropdown-segmentos", "value"),
            Input("start-button", "n_clicks"),
        ],
        [State("annotate-button", "n_clicks"), ]
    )
    def display_scatter_plot(dataset, segmentos, start, annotate):
        data = data_dict['DODF2D']
        df = pd.DataFrame(data)
        if annotate == 0:
            if dataset == "DODF_Aposentadoria":
                if segmentos == "2018":
                    data = data_dict['Aposentadoria']['DODF_Aposentadoria2018']
                    df = pd.DataFrame(data)
                elif segmentos == "2019":
                    data = data_dict['Aposentadoria']['DODF_Aposentadoria2019']
                    df = pd.DataFrame(data)
                else:
                    data = data_dict['Aposentadoria']['DODF_Aposentadoria2D']
                    df = pd.DataFrame(data)

            elif dataset == "DODF_Editais":
                if segmentos == "2013":
                    data = data_dict['Editais']['DODF_Editais2013']
                    df = pd.DataFrame(data)
                elif segmentos == "2014":
                    data = data_dict['Editais']['DODF_Editais2014']
                    df = pd.DataFrame(data)
                elif segmentos == "2015":
                    data = data_dict['Editais']['DODF_Editais2015']
                    df = pd.DataFrame(data)
                elif segmentos == "2016":
                    data = data_dict['Editais']['DODF_Editais2016']
                    df = pd.DataFrame(data)
                elif segmentos == "2017":
                    data = data_dict['Editais']['DODF_Editais2017']
                    df = pd.DataFrame(data)
                elif segmentos == "2018":
                    data = data_dict['Editais']['DODF_Editais2018']
                    df = pd.DataFrame(data)
                elif segmentos == "2019":
                    data = data_dict['Editais']['DODF_Editais2019']
                    df = pd.DataFrame(data)
                elif segmentos == "2020":
                    data = data_dict['Editais']['DODF_Editais2020']
                    df = pd.DataFrame(data)
                elif segmentos == "outros":
                    data = data_dict['Editais']['DODF_Editaisoutros']
                    df = pd.DataFrame(data)
                else:
                    data = data_dict['Editais']['DODF_Editais2D']
                    df = pd.DataFrame(data)

            elif dataset == "DODF_Exoneracoes":
                if segmentos == "2010":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2010']
                    df = pd.DataFrame(data)
                elif segmentos == "2011":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2011']
                    df = pd.DataFrame(data)
                elif segmentos == "2012":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2012']
                    df = pd.DataFrame(data)
                elif segmentos == "2013":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2013']
                    df = pd.DataFrame(data)
                elif segmentos == "2014":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2014']
                    df = pd.DataFrame(data)
                elif segmentos == "2015":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2015']
                    df = pd.DataFrame(data)
                elif segmentos == "2016":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2016']
                    df = pd.DataFrame(data)
                elif segmentos == "2017":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2017']
                    df = pd.DataFrame(data)
                elif segmentos == "2018":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2018']
                    df = pd.DataFrame(data)
                elif segmentos == "2019":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2019']
                    df = pd.DataFrame(data)
                elif segmentos == "2020":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2020']
                    df = pd.DataFrame(data)
                else:
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2D']
                    df = pd.DataFrame(data)

            else:
                data = data_dict['DODF2D']
                df = pd.DataFrame(data)

            figure = generate_figure_TSNE(df)

        if annotate != 0:
            figure = generate_figure_TSNE(dfAnno)

        return (figure)

    @app.callback(
        Output("selected-point", "children"),

        [
            Input("graph-3d-plot-tsne", "clickData"),
        ],
        [
            State("dropdown-dataset", "value"),
            State("annotate-button", "n_clicks")
        ]
    )
    def explore_data(clickData, dataset, annotate):

        if dataset == "DODF_Aposentadoria":
            data = data_dict['Aposentadoria']['DODF_Aposentadoria2D']
            df = pd.DataFrame(data)

        elif dataset == "DODF_Editais":
            data = data_dict['Editais']['DODF_Editais2D']
            df = pd.DataFrame(data)

        elif dataset == "DODF_Exoneracoes":
            data = data_dict['Exoneracoes']['DODF_Exoneracoes2D']
            df = pd.DataFrame(data)
        else:
            data = data_dict['DODF2D']
            df = pd.DataFrame(data)

        if annotate:
            df = dfAnno

        contents = []

        contents.append(
            html.Div(
                children=[
                    html.H5(
                        "Clique em um ponto para visualizar o texto do ato selecionado."),

                    html.Div(
                        style={"width": "100%", "height": "80vh",
                               "display": "grid", "place-items": "center"},
                        children=[
                            html.Img(
                                src=app.get_asset_url("knedle-logo4.png"),
                                style={"height": "100px", "opacity": "0.5"},
                            )
                        ]
                    )
                ]
            )
        )

        if clickData:

            XY = {}
            XY['x'] = clickData["points"][0]['x']
            XY['y'] = clickData["points"][0]['y']
            achar_indice = (df.loc[:, "x":"y"].eq(XY).all(axis=1))

            # Retrieve the index of the point clicked, given it is present in the set
            if achar_indice.any():

                clicked_idx = df[achar_indice].index[0]
                label = df['label'][clicked_idx]
                contents = []

                if dataset == "DODF_Aposentadoria":
                    ref_anomes = df['REF_ANOMES'][clicked_idx]
                    data_dodf = df['DATA_DODF'][clicked_idx]
                    num_dodf = df['NUM_DODF'][clicked_idx]
                    pagina_dodf = df['PAGINA_DODF'][clicked_idx]
                    tipo_dodf = df['TIPO_DODF'][clicked_idx]
                    ato = df['ATO'][clicked_idx]
                    empresa_ato = df['EMPRESA_ATO'][clicked_idx]
                    cod_matricula_ato = df['COD_MATRICULA_ATO'][clicked_idx]
                    cod_matricula_sigrh = df['COD_MATRICULA_SIGRH'][clicked_idx]
                    nome_ato = df['NOME_ATO'][clicked_idx]
                    cargo = df['CARGO'][clicked_idx]
                    classe = df['CLASSE'][clicked_idx]
                    padrao = df['PADRAO'][clicked_idx]
                    quadro = df['QUADRO'][clicked_idx]
                    processo = df['PROCESSO'][clicked_idx]
                    fund_legal = df['FUND_LEGAL'][clicked_idx]

                    contents.append(html.H5(label))
                    contents.append(
                        html.Ul(
                            style={"list-style-type": "none",
                                   "margin-bottom": "1px"},
                            className="list",
                            children=[
                                (html.Li("REF_ANOMES: " + str(ref_anomes))),
                                (html.Li("DATA_DODF: " + str(data_dodf))),
                                (html.Li("NUM_DODF: " + str(num_dodf))),
                                (html.Li("PAGINA_DODF: " + str(pagina_dodf))),
                                (html.Li("TIPO_DODF: " + str(tipo_dodf))),
                                (html.Li("ATO: " + str(ato))),
                                (html.Li("EMPRESA_ATO: " + str(empresa_ato))),
                                (html.Li("COD_MATRICULA_ATO: " + str(cod_matricula_ato))),
                                (html.Li("COD_MATRICULA_SIGRH: " +
                                         str(cod_matricula_sigrh))),
                                (html.Li("NOME_ATO: " + str(nome_ato))),
                                (html.Li("CARGO: " + str(cargo))),
                                (html.Li("CLASSE: " + str(classe))),
                                (html.Li("PADRAO: " + str(padrao))),
                                (html.Li("QUADRO: " + str(quadro))),
                                (html.Li("PROCESSO: " + str(processo))),
                                (html.Li("FUND_LEGAL: " + str(fund_legal))),
                            ]
                        )
                    )

                elif dataset == "DODF_Editais":
                    idEditais = df['idEditais'][clicked_idx]
                    autuado = df['autuado'][clicked_idx]
                    nrEdital = df['nrEdital'][clicked_idx]
                    anoEdital = df['anoEdital'][clicked_idx]
                    siglaLicitante = df['siglaLicitante'][clicked_idx]
                    nomeLicitante = df['nomeLicitante'][clicked_idx]
                    dtPublicacao = df['dtPublicacao'][clicked_idx]
                    nrDodf = df['nrDodf'][clicked_idx]
                    anoDodf = df['anoDodf'][clicked_idx]
                    dtAbertura = df['dtAbertura'][clicked_idx]
                    modalidadeLicitacao = df['modalidadeLicitacao'][clicked_idx]
                    vrEstimado = df['vrEstimado'][clicked_idx]
                    prazo = df['prazo'][clicked_idx]
                    prazoAbertura = df['prazoAbertura'][clicked_idx]
                    tpPrazo = df['tpPrazo'][clicked_idx]
                    ementaObj = df['ementaObj'][clicked_idx]
                    descObjeto = df['descObjeto'][clicked_idx]
                    nrgdf = df['nrgdf'][clicked_idx]
                    anogdf = df['anogdf'][clicked_idx]
                    classifObjeto = df['classifObjeto'][clicked_idx]

                    contents.append(html.H5(label))
                    contents.append(
                        html.Ul(
                            style={"list-style-type": "none",
                                   "margin-bottom": "1px"},
                            className="list",
                            children=[
                                (html.Li("idEditais: " + str(idEditais))),
                                (html.Li("autuado: " + str(autuado))),
                                (html.Li("nrEdital: " + str(nrEdital))),
                                (html.Li("anoEdital: " + str(anoEdital))),
                                (html.Li("siglaLicitante: " + str(siglaLicitante))),
                                (html.Li("nomeLicitante: " + str(nomeLicitante))),
                                (html.Li("dtPublicacao: " + str(dtPublicacao))),
                                (html.Li("nrDodf: " + str(nrDodf))),
                                (html.Li("anoDodf: " + str(anoDodf))),
                                (html.Li("dtAbertura: " + str(dtAbertura))),
                                (html.Li("modalidadeLicitacao: " +
                                         str(modalidadeLicitacao))),
                                (html.Li("vrEstimado: " + str(vrEstimado))),
                                (html.Li("prazo: " + str(prazo))),
                                (html.Li("prazoAbertura: " + str(prazoAbertura))),
                                (html.Li("tpPrazo: " + str(tpPrazo))),
                                (html.Li("ementaObj: " + str(ementaObj))),
                                (html.Li("descObjeto: " + str(descObjeto))),
                                (html.Li("nrgdf: " + str(nrgdf))),
                                (html.Li("anogdf: " + str(anogdf))),
                                (html.Li("classifObjeto: " + str(classifObjeto))),
                            ]
                        )
                    )

                elif dataset == "DODF_Exoneracoes":
                    NOME_DO_SERVIDOR = df['01_NOME_DO_SERVIDOR'][clicked_idx]
                    MATRICULA = df['02_MATRICULA'][clicked_idx]
                    CARGO_COMISSAO_SIMBOLO = df['03_CARGO_COMISSAO_SIMBOLO'][clicked_idx]
                    CARGO_COMISSAO = df['04_CARGO_COMISSAO'][clicked_idx]
                    LOTACAO = df['05_LOTACAO'][clicked_idx]
                    LOTACAO_SUPERIOR_1 = df['05_LOTACAO_SUPERIOR_1'][clicked_idx]
                    LOTACAO_SUPERIOR_2 = df['05_LOTACAO_SUPERIOR_2'][clicked_idx]
                    LOTACAO_SUPERIOR_3 = df['05_LOTACAO_SUPERIOR_3'][clicked_idx]
                    LOTACAO_SUPERIOR_4 = df['05_LOTACAO_SUPERIOR_4'][clicked_idx]
                    ORGAO = df['06_ORGAO'][clicked_idx]
                    VIGENCIA = df['07_VIGENCIA'][clicked_idx]
                    A_PEDIDO = df['08_A_PEDIDO'][clicked_idx]
                    CARGO_EFETIVO = df['09_CARGO_EFETIVO'][clicked_idx]
                    CARGO_EFETIVO_REFERENCIA = df['09_CARGO_EFETIVO_REFERENCIA'][clicked_idx]
                    MATRICULA_SIAPE = df['10_MATRICULA_SIAPE'][clicked_idx]
                    MOTIVO = df['11_MOTIVO'][clicked_idx]

                    contents.append(html.H5(label))
                    contents.append(
                        html.Ul(
                            style={"list-style-type": "none",
                                   "margin-bottom": "1px"},
                            className="list",
                            children=[
                                (html.Li("NOME_DO_SERVIDOR: " + str(NOME_DO_SERVIDOR))),
                                (html.Li("MATRICULA: " + str(MATRICULA))),
                                (html.Li("CARGO_COMISSAO_SIMBOLO: " +
                                         str(CARGO_COMISSAO_SIMBOLO))),
                                (html.Li("CARGO_COMISSAO: " + str(CARGO_COMISSAO))),
                                (html.Li("LOTACAO: " + str(LOTACAO))),
                                (html.Li("LOTACAO_SUPERIOR_1: " +
                                         str(LOTACAO_SUPERIOR_1))),
                                (html.Li("LOTACAO_SUPERIOR_2: " +
                                         str(LOTACAO_SUPERIOR_2))),
                                (html.Li("LOTACAO_SUPERIOR_3: " +
                                         str(LOTACAO_SUPERIOR_3))),
                                (html.Li("LOTACAO_SUPERIOR_4: " +
                                         str(LOTACAO_SUPERIOR_4))),
                                (html.Li("ORGAO: " + str(ORGAO))),
                                (html.Li("VIGENCIA: " + str(VIGENCIA))),
                                (html.Li("A_PEDIDO: " + str(A_PEDIDO))),
                                (html.Li("CARGO_EFETIVO: " + str(CARGO_EFETIVO))),
                                (html.Li("CARGO_EFETIVO_REFERENCIA: " +
                                         str(CARGO_EFETIVO_REFERENCIA))),
                                (html.Li("MATRICULA_SIAPE: " + str(MATRICULA_SIAPE))),
                                (html.Li("MOTIVO: " + str(MOTIVO))),
                            ]
                        )
                    )

                else:

                    conteudo = df['conteudo'][clicked_idx]
                    contents.append(html.H5(label))
                    contents.append(html.P(conteudo))

            else:
                contents = []
                contents.append(
                    html.Div(
                        children=[
                            html.H5(
                                "Clique em um ponto para visualizar o texto do ato selecionado."),

                            html.Div(
                                style={"width": "100%", "height": "80vh",
                                       "display": "grid", "place-items": "center"},
                                children=[
                                    html.Img(
                                        src=app.get_asset_url(
                                            "knedle-logo4.png"),
                                        style={"height": "100px",
                                               "opacity": "0.5"},
                                    )
                                ]
                            )
                        ]
                    )
                )

        return contents

    @app.callback(
        [
            Output("explore-data", "style"),
            Output("annotate-data", "style"),
        ],
        [
            Input("annotate-button", "n_clicks"),
        ],
        [
            State("dropdown-dataset", "value"),
            State("dropdown-segmentos", "value")
        ]
    )
    def set_annotate_data(click, dataset, segmentos):
        global dfAnno
        if click == 1:
            if dataset == "DODF_Aposentadoria":
                if segmentos == "2018":
                    data = data_dict['Aposentadoria']['DODF_Aposentadoria2018']
                    df = pd.DataFrame(data)
                elif segmentos == "2019":
                    data = data_dict['Aposentadoria']['DODF_Aposentadoria2019']
                    df = pd.DataFrame(data)
                else:
                    data = data_dict['Aposentadoria']['DODF_Aposentadoria2D']
                    df = pd.DataFrame(data)

            elif dataset == "DODF_Editais":
                if segmentos == "2013":
                    data = data_dict['Editais']['DODF_Editais2013']
                    df = pd.DataFrame(data)
                elif segmentos == "2014":
                    data = data_dict['Editais']['DODF_Editais2014']
                    df = pd.DataFrame(data)
                elif segmentos == "2015":
                    data = data_dict['Editais']['DODF_Editais2015']
                    df = pd.DataFrame(data)
                elif segmentos == "2016":
                    data = data_dict['Editais']['DODF_Editais2016']
                    df = pd.DataFrame(data)
                elif segmentos == "2017":
                    data = data_dict['Editais']['DODF_Editais2017']
                    df = pd.DataFrame(data)
                elif segmentos == "2018":
                    data = data_dict['Editais']['DODF_Editais2018']
                    df = pd.DataFrame(data)
                elif segmentos == "2019":
                    data = data_dict['Editais']['DODF_Editais2019']
                    df = pd.DataFrame(data)
                elif segmentos == "2020":
                    data = data_dict['Editais']['DODF_Editais2020']
                    df = pd.DataFrame(data)
                elif segmentos == "outros":
                    data = data_dict['Editais']['DODF_Editaisoutros']
                    df = pd.DataFrame(data)
                else:
                    data = data_dict['Editais']['DODF_Editais2D']
                    df = pd.DataFrame(data)

            elif dataset == "DODF_Exoneracoes":
                if segmentos == "2010":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2010']
                    df = pd.DataFrame(data)
                elif segmentos == "2011":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2011']
                    df = pd.DataFrame(data)
                elif segmentos == "2012":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2012']
                    df = pd.DataFrame(data)
                elif segmentos == "2013":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2013']
                    df = pd.DataFrame(data)
                elif segmentos == "2014":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2014']
                    df = pd.DataFrame(data)
                elif segmentos == "2015":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2015']
                    df = pd.DataFrame(data)
                elif segmentos == "2016":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2016']
                    df = pd.DataFrame(data)
                elif segmentos == "2017":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2017']
                    df = pd.DataFrame(data)
                elif segmentos == "2018":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2018']
                    df = pd.DataFrame(data)
                elif segmentos == "2019":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2019']
                    df = pd.DataFrame(data)
                elif segmentos == "2020":
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2020']
                    df = pd.DataFrame(data)
                else:
                    data = data_dict['Exoneracoes']['DODF_Exoneracoes2D']
                    df = pd.DataFrame(data)

            else:
                data = data_dict['DODF2D']
                df = pd.DataFrame(data)

            dfAnno = df
            return {"display": "none"}, {"display": "grid", "grid-template-columns": "70% 15% auto"}
        else:
            return {"display": "grid", "grid-template-columns": "70% 30%"}, {"display": "none"}

    @app.callback(
    [
        Output("help", "style"),
        Output("help-button", "children")
    ],
    [
        Input("help-button", "n_clicks")
    ]
    )
    def display_help(clicks):
        if clicks is None:
            clicks = 0
        if (clicks % 2) == 1:
            clicks += 1
            return (
                {},
                "Close Help",
            )
        else:
            clicks += 1
            return (
                {"display": "none"},
                html.I(className="fas fa-2x fa-question-circle"),
            )

    @app.callback(
        [
            Output("insert-new-label", "style"),
        ],
        [
            Input("dropdown-label", "value"),
        ])
    def display_new_label(value):
        if value == "add_label":
            return [{"display": "grid", "grid-template-columns": "100px 150px 75px", "margin-left": "20px"}]
        else:
            return [{"display": "none"}]

    @app.callback(
        [
            Output("dropdown-label", "options"),
            Output("dropdown-label", "value"),
        ],
        [
            Input("submit-button", "n_clicks"),
        ],
        [
            State("input-new-label", "value"),
            State("dropdown-label", "options"),
            State("dropdown-label", "value"),
            State("annotate-button", "n_clicks")
        ])
    def add_new_label(clicks, new_label, options, label, annotate):
        if annotate != 0:
            temp_options = options
            temp_options.append({"label": new_label, "value": new_label})
            return temp_options, new_label
        else:
            return options, label

    @app.callback(
        [
            Output("qnt-annotations", "children"),
            Output("start-button", "children"),
        ],
        [
            Input("start-button", "n_clicks"),
        ],
        [
            State("graph-3d-plot-tsne", "clickData"),
            State("graph-3d-plot-tsne", "selectedData"),
            State("dropdown-label", "value")
        ]
    )
    def annotate_data(start, clickData, selectedData, label_value):
        global dfAnno
        df = dfAnno

        if selectedData and label_value != "add_label":
            clickData = 0
            j = 0
            for point in selectedData["points"]:
                XY = {}
                XY['x'] = selectedData["points"][j]['x']
                XY['y'] = selectedData["points"][j]['y']
                achar_indice = (df.loc[:, "x":"y"].eq(XY).all(axis=1))
                clicked_idx = df[achar_indice].index[0]
                df.at[clicked_idx, 'label'] = label_value
                j += 1

        if clickData and label_value != "add_label":
            XY = {}
            XY['x'] = clickData["points"][0]['x']
            XY['y'] = clickData["points"][0]['y']
            achar_indice = (df.loc[:, "x":"y"].eq(XY).all(axis=1))
            clicked_idx = df[achar_indice].index[0]
            df.at[clicked_idx, 'label'] = label_value

        dfAnno = df

        i = 0
        qnt = 0
        while i < len(df):
            if df["label"][i] != "Unlabeled":
                qnt += 1
            i += 1

        return html.H6("Annotate (" + str(qnt) + ")"), "Annotate"

    @app.callback(
        Output('download', 'children'),
        [Input("finish-button", "n_clicks")]
    )
    def donwload_annotation(click):
        contents = []
        if click:
            df = dfAnno
            df = df.drop(columns=["Unnamed: 0", "x", "y"])
            df.to_csv("annotation.csv", index=False)

            i = 0
            qnt = 0
            while i < len(dfAnno):
                if dfAnno["label"][i] != "Unlabeled":
                    qnt += 1
                i += 1
            contents = []
            contents.append(
                html.H4(children=["Your csv file:"], className='text-act'))
            contents.append(
                html.H5(children=["Number of annotations: " + str(qnt)], className='text-ocu'))
            contents.append(dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'name': i, 'id': i} for i in df.columns],
                            style_cell={
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'maxWidth': '50px',
                                'height': 'auto'
                            },
                            style_table={
                                'maxHeight': '700px',
                                'overflowY': 'scroll',
                                'overflowX': 'auto',
                                'marginBottom': '40px'
                            }
                            ))

        return html.Div(contents)

    @app.callback(
        [
            Output('homepage', 'style'),
            Output('download-page', 'style'),
        ],
        [
            Input("finish-button", "n_clicks"),
            Input("return-button", "n_clicks"),
        ]

    )
    def donwload_annotation_page(finish, return_click):
        if return_click:
            return [
                {"padding": "15px", "display": "grid", "grid-template-columns": "auto 400px",
                    "height": "95vh", "margin-bottom": "5px"},
                {"display": "none"}
            ]

        if finish == 0:
            return [
                {"padding": "15px", "display": "grid", "grid-template-columns": "auto 400px",
                    "height": "95vh", "margin-bottom": "5px"},
                {"display": "none"}
            ]

        else:
            return [
                {"display": "none"},
                {"padding": "15px", "display": "block",
                    "height": "95vh", "margin-bottom": "5px"},
            ]

    @app.callback(
        [
            Output("return-button", "n_clicks"),
            Output("help-button", "n_clicks"),
        ],
        [
            Input("finish-button", "n_clicks"),
        ])
    def reset_download(finish):
        return 0, 0

    @app.callback(
        [
            Output("finish-button", "n_clicks"),
            Output("annotate-button", "n_clicks"),
            Output("start-button", "n_clicks"),
        ],
        [
            Input("end-button", "n_clicks"),
        ])
    def reset_end(end):
        return 0, 0, 0

    @app.callback(
        Output('download-link', 'href'),
        [Input('download-button', 'n_clicks')])
    def update_download_link(filter_value):
        dff = dfAnno
        csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string)
        return csv_string


# cores
#vermelho: rgb(196, 59, 35)
#verde: rgb(135, 202, 59)
