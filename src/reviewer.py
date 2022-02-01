from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

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

def callbacks(app):
    @app.callback(
        [   
            Output("page-content", "children"), 
        ],
        [
            Input("url", "pathname")
        ], 
        [
            State("reviewer_select","children"),
            State("reviewer_correct","children"),
            State("reviewer_download","children")
        ])
    def render_page_content(pathname, select, correct, download):
        if pathname == "/":
            return select
        elif pathname == "/correct":
            return correct
        elif pathname == "/dowload":
            return download

        return select


    @app.callback(
        [   
            Output("reviewer_point_visualization", "style"),
            Output("reviewer_list_visualization", "style"), 
        ],
        [
            Input("view_switch", "value")
        ], 
    )
    def change_view(view_list):
        if view_list:
            return [{'display':'none'},{}]
        return [{},{'display':'none'}]

    def _generate_figure(df,level,color_code):
        
        X = 'x_tsne'
        Y = 'y_tsne'

        entity = False
        if level:
            entity = True

        tags = True
        if color_code:
            tags = False        

        if entity:
            if tags:
                figure = px.scatter(df, x=X, y=Y,hover_name='texto_ent', color = 'tipo_ent',color_discrete_sequence=px.colors.qualitative.Pastel)
            else:
                figure = px.scatter(df, x=X, y=Y,hover_name='texto_ent', color = 'temp_estado_visnote',color_discrete_map=colors)
                    
            figure.update_layout(legend=dict(orientation="v",yanchor="top",y=1,xanchor="left",x=1,title=dict(text="Legenda", font=dict(family="Arial", size=22), side="top"),valign="top",itemclick="toggleothers",),yaxis={'visible': False, 'showticklabels': False},xaxis={'visible': False, 'showticklabels': False},margin=dict(l=10, r=10, t=20, b=5))


        else:
            if tags:
                COLOR = 'tipo_rel'
            else:
                COLOR = 'temp_estado_visnote'
            
            figure = px.scatter(df, x=X, y=Y, color = COLOR,color_discrete_map=colors)
            figure.update_layout(showlegend=False, yaxis={'visible': False, 'showticklabels': False}, xaxis={'visible': False, 'showticklabels': False}, margin=dict(l=10, r=10, t=20, b=5) )

        figure.update_traces(marker=dict(line=dict(width=1, color='white')),)
            
        return figure

    @app.callback(
        [   
            Output("point_visualization", "figure"),
        ],
        [
            Input("level_switch", "value"),
            Input("color_code_switch", "value"),
            Input("value-button_review_annotations", "n_clicks"),
        ], 
    )
    def update_point_visualization(level, color_code, run):
        if level:
            df = pd.read_csv('./data/list_annotations.csv')
        else:
            df = pd.read_csv('./data/list_relations.csv')

        figure = _generate_figure(df, level, color_code)

        return [figure]

    