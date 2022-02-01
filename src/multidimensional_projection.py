from .preprocessing import preprocess

import csv
import pandas as pd
import re
import nltk

from dash.dependencies import Input, Output

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import umap.umap_ as umap
import plotly.express as px

def run_tfidf(text):
    corpus = list(text)
    tfidf = TfidfVectorizer() 
    tfidf.fit(corpus)
    tfidf_result = tfidf.transform(corpus)
    return tfidf_result

def run_tsne(tfidf):
    tsne = TSNE(perplexity=100,learning_rate=100)
    tsne_results = tsne.fit_transform(tfidf)
    df_tsne = pd.DataFrame(tsne_results, columns=["x", "y"])
    
    return df_tsne

def run_umap(tfidf):
    reducer = umap.UMAP(n_neighbors=100, min_dist=0.99,metric='cosine')
    embedding = reducer.fit_transform(tfidf)

    x = list(embedding[:,0])
    y = list(embedding[:,1])

    df_umap = pd.DataFrame(x, columns=["x"])
    df_umap['y'] = y
    
    return df_umap

def projecao_multi(df, text_column):
    result = preprocess(df, text_column)
    text = result.texto_temp
    
    result = result.drop(columns=['texto_temp'])
    tfidf = run_tfidf(text)
    
    df_tsne = run_tsne(tfidf)    
    #df_umap = run_umap(tfidf)
    
    result["x_tsne"] = df_tsne.x
    result["y_tsne"] = df_tsne.y

    estado = []
    for i in range(len(result)):
        estado.append('nao_confirmado')

    result['temp_estado_visnote'] = estado

    #result["x_umap"] = df_umap.x
    #result["y_umap"] = df_umap.y
      
    return result

def callbacks(app):
    @app.callback(
        [    
            Output("value-button_review_annotations", "n_clicks"),
        ],
        [
            Input("button_review_annotations", "n_clicks")
        ]    
    )
    def run_tsne_umap(run):
        if run:
            relacoes = pd.read_csv("./data/original_relations.csv")
            mdp_relacoes = projecao_multi(relacoes, 'texto') 
            mdp_relacoes.to_csv("./data/list_relations.csv",index=False)
            entidades = pd.read_csv("./data/original_annotations.csv")
            mdp_entidades = projecao_multi(entidades, 'texto_ent') 
            mdp_entidades.to_csv("./data/list_annotations.csv",index=False)

            return [1]
        return [0]


