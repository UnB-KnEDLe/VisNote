import csv
import pandas as pd
import re
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
nltk.download('stopwords')
nltk.download('punkt')

from sklearn.manifold import TSNE
import umap.umap_ as umap
import plotly.express as px

stop_list = nltk.corpus.stopwords.words('portuguese')

def cleanText(text):
    text = text.lower()
    text = re.sub(r"á", "a", text)
    text = re.sub(r"â", "a", text)
    text = re.sub(r"à", "a", text)
    text = re.sub(r"ã", "a", text)
    text = re.sub(r"é", "e", text)
    text = re.sub(r"ê", "e", text)
    text = re.sub(r"í", "i", text)
    text = re.sub(r"ó", "o", text)
    text = re.sub(r"ô", "o", text)
    text = re.sub(r"õ", "o", text)
    text = re.sub(r"ú", "u", text)
    text = re.sub(r"ç", "c", text)
    text = re.sub(r"[^a-zA-Z ]", "", text)
    text = re.sub(r"\\W", "", text)
    text = re.sub(r"\\s+", "", text)
    text = text.strip(' ')
    return text

def remove_stopwords(tokens):
    return [token for token in tokens if token.lower() not in stop_list] 

def preprocess(df):
    textos = []
    textos_clean = []
    i = 0
    while i < len(df.conteudo):
        if len(df.conteudo[i]) > 0:
            textos.append(df.conteudo[i])
        else:
            textos.append("nan")
        i += 1

    i = 0
    while i < len(textos):
        textos_clean.append(cleanText(textos[i]))
        i += 1

    text_tokens = [nltk.word_tokenize(doc) for doc in textos_clean]

    text_stop = [' '.join(remove_stopwords(doc)) for doc in text_tokens]
    
    return text_stop

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
    reducer = umap.UMAP(n_neighbors=100, min_dist=0.8,metric='euclidean')
    embedding = reducer.fit_transform(tfidf)

    x = list(embedding[:,0])
    y = list(embedding[:,1])

    df_umap = pd.DataFrame(x, columns=["x"])
    df_umap['y'] = y
    
    return df_umap

def projecao_multi(df):
    text = preprocess(df)
    tfidf = run_tfidf(text)
    
    df_tsne = run_tsne(tfidf)
    df_tsne['tipo'] = df.tipo 
    
    df_umap = run_tsne(tfidf)
    df_umap['tipo'] = df.tipo
    
    result = pd.DataFrame()
    result["x_tsne"] = df_tsne.x
    result["y_tsne"] = df_tsne.y
    result["x_umap"] = df_umap.x
    result["y_umap"] = df_umap.y
    result["cod"] = df.cod
    result["documento"] = df.documento
    result["id"] = df.id
    result["anotador"] = df.anotador
    result["tipo"] = df.tipo
    result["conteudo"] = df.conteudo
    result["estado"] = df.estado
    
    
    return result
    
