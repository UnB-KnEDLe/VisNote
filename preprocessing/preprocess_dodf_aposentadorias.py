import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import plotly.express as px

data = pd.read_csv("dodfAposentadorias.csv")

# Preprocess

conteudo = []
colunas = ["REF_ANOMES", "DATA_DODF", "NUM_DODF", "PAGINA_DODF", "TIPO_DODF", 'ATO', 'EMPRESA_ATO', 'COD_MATRICULA_ATO', 'COD_MATRICULA_SIGRH', 'NOME_ATO', 'CARGO', 'CLASSE', 'PADRAO', 'QUADRO', 'PROCESSO', 'FUND_LEGAL']
string = ""

i = 0
while i < len(data):
    for coluna in colunas:
        X = data[coluna][i]
        string = string + str(X) + ' '
    
    
    conteudo.append(string)
    string = ''
    i = i + 1

data['conteudo'] = conteudo

text = data["conteudo"]

# TF-IDF

corpus = list(text)
tfidf = TfidfVectorizer(max_features = 6000) 
tfidf.fit(corpus)
tfidf_features = tfidf.transform(corpus)

# t-SNE 

pca_dim = 50
iterations = 500
learning_rate = 100
perplexity = 50

nb_col = tfidf_features.shape[1]

pca = PCA(n_components=min(nb_col, pca_dim))

tfidf_dense = tfidf_features.toarray() 
data_pca = pca.fit_transform(tfidf_dense)

tsne = TSNE(
    n_components=2,
    n_iter=iterations,
    learning_rate=learning_rate,
    perplexity=perplexity,
    random_state=1131,
)

DODF_tsne = tsne.fit_transform(data_pca)

df = pd.DataFrame(DODF_tsne, columns=["x", "y"])

# Unlabel

df = pd.DataFrame(DODF_tsne, columns=["x", "y"])

label = []
i=0
while i < len(df):
    label.append("Unlabeled")
    i += 1
df["label"] = label

df = pd.concat([df, data], axis=1, sort=False)

# Segmentation

colunas = ['x', 'y', 'label', 'REF_ANOMES', 'DATA_DODF', 'NUM_DODF', 'PAGINA_DODF',
       'TIPO_DODF', 'ATO', 'COD_EMPRESA', 'EMPRESA_ATO', 'COD_MATRICULA_ATO',
       'COD_MATRICULA_SIGRH', 'NOME_ATO', 'NOME_SIGRH', 'CARGO',
       'CLASSE', 'PADRAO', 'QUADRO', 'PROCESSO', 'FUND_LEGAL', 'conteudo']


row = {}
for x in colunas:
    row[x] = "NaN"
    
df2018 = pd.DataFrame(columns = colunas)
df2019 = pd.DataFrame(columns = colunas)
dfoutros = pd.DataFrame(columns = colunas)


i=0
while i < len(df):
    k = 0
    ano = str(df['DATA_DODF'][i])
    if ano[:4] == "2018":
        for x in colunas:
            row[x] = "NaN"
        #para cada atributo, adicionar a ao dicionário
        for j in df.loc[i]:
            row[colunas[k]] = j
            k += 1
        df2018 = df2018.append(row, ignore_index=True)
    elif ano[:4] == "2019":
        for x in colunas:
            row[x] = "NaN"
        #para cada atributo, adicionar a ao dicionário
        for j in df.loc[i]:
            row[colunas[k]] = j
            k += 1
        df2019 = df2019.append(row, ignore_index=True)
    else:
        for x in colunas:
            row[x] = "NaN"
        for j in df.loc[i]:
            row[colunas[k]] = j
            k += 1
        dfoutros = dfoutros.append(row, ignore_index=True)
    i+=1

# Save dataframes in CSV files

df.to_csv("DODF_Aposentadoria2D.csv")
df2018.to_csv("DODF_Aposentadoria_2018.csv")
df2019.to_csv("DODF_Aposentadoria_2019.csv")
