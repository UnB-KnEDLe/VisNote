import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import plotly.express as px

data = pd.read_csv("dodftrain.csv")

text = data["text"]

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

df["conteudo"] = text

label = []
i=0
while i < len(df):
    label.append("Unlabeled")
    i += 1
df["label"] = label

# Save the dataframe in a CSV file

df.to_csv("dodf.csv")