from preprocessing import preprocess

import csv
import pandas as pd
import re
import nltk
import spacy


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

def projecao_multi(df):
    result = preprocess(df)
    text = result.texto_temp
    
    result = result.drop(columns=['texto_temp'])
    tfidf = run_tfidf(text)
    
    df_tsne = run_tsne(tfidf)    
    df_umap = run_umap(tfidf)
    
    result["x_tsne"] = df_tsne.x
    result["y_tsne"] = df_tsne.y
    result["x_umap"] = df_umap.x
    result["y_umap"] = df_umap.y
      
    return result

  
