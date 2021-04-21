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

def find_entidades(df,j):
    entidades = []
    i = 0
    while i < len(df.texto):
        if df.id_dodf_rel[i] == df.id_dodf_rel[j]:
            entidades.append(df.id_geral[i])
        i += 1
    return entidades

def preprocess(df):
    colunas = ['id_geral', 'id_dodf_rel','tipo_rel','estado_rel','texto','anotacoes']
    df_result = pd.DataFrame(columns = colunas)
    
    dictAux = {'id_geral':'x', 'id_dodf_rel':'x','tipo_rel':'x','estado_rel':'x','texto':'x','anotacoes':[]}
    tipos_atos = ['Ato_Abono_Permanencia','Ato_Aposentadoria','Ato_Cessao','Ato_Exoneracao_Comissionado','Ato_Exoneracao_Efetivo','Ato_Nomeacao_Comissionado','Ato_Nomeacao_Efetivo','Ato_Retificacao_Comissionado','Ato_Retificacao_Efetivo','Ato_Reversao','Ato_Substituicao','Ato_Tornado_Sem_Efeito_Apo','Ato_Tornado_Sem_Efeito_Exo_Nom']
    textos = []
    textos_clean = []
    i = 0
    while i < len(df.texto):
        if (len(df.texto[i]) > 0) and (df.tipo_ent[i] in tipos_atos):
            dictAux["id_geral"] = df.id_geral[i]    
            dictAux["id_dodf_rel"] = df.id_dodf_rel[i]
            dictAux["tipo_rel"] = df.tipo_rel[i]
            dictAux["estado_rel"] = 'nao_confirmado'
            dictAux["texto"] = df.texto[i]
            dictAux["anotacoes"] = find_entidades(df,i)
            df_length = len(df_result)
            df_result.loc[df_length] = dictAux
                                
            textos.append(df.texto[i])
        i += 1

    i = 0
    while i < len(textos):
        textos_clean.append(cleanText(textos[i]))
        i += 1

    text_tokens = [nltk.word_tokenize(doc) for doc in textos_clean]

    text_stop = [' '.join(remove_stopwords(doc)) for doc in text_tokens]
    
    df_result['texto_temp'] = text_stop
    
    return df_result

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
    df_umap = run_tsne(tfidf)
    
    result["x_tsne"] = df_tsne.x
    result["y_tsne"] = df_tsne.y
    result["x_umap"] = df_umap.x
    result["y_umap"] = df_umap.y
      
    return result
    
