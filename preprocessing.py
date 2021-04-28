import csv
import pandas as pd
import re
import nltk
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')
nltk.download('punkt')

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
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    text = re.sub(r"\\W", "", text)
    text = re.sub(r"\\s+", "", text)
    #text = re.sub(r"\n", " ", text)
    text = text.strip(' ')
    return text

def remove_stopwords(tokens):
    
    stop_list = nltk.corpus.stopwords.words('portuguese')
    return [token for token in tokens if token.lower() not in stop_list] 

def preprocess(df):
    
    textos_clean = []
    
    for i in df.texto:
        textos_clean.append(cleanText(i))       

    text_tokens = [nltk.word_tokenize(doc) for doc in textos_clean]

    text_stop = [' '.join(remove_stopwords(doc)) for doc in text_tokens]
    
    df['texto_temp'] = text_stop
    
    return df