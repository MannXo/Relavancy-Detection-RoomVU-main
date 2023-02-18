import csv
import sqlite3
import pandas as pd
import spacy
from config import DB_PATH
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
import nltk
from imblearn.over_sampling import SMOTE
filename = r"train.csv"
df = pd.read_csv(filename) 

nltk.download('punkt')
sp = spacy.load('en_core_web_sm')
all_stopwords = sp.Defaults.stop_words
stemmer = PorterStemmer()
# cleaning
for i, row in df.iterrows():
    title_txt = row['Title'].lower()
    text_tokens = word_tokenize(title_txt)
    text_tokens_stemmed = [stemmer.stem(token) for token in text_tokens]
    title_txt = " ".join(text_tokens_stemmed)
    snippet_txt = row['Snippet'].lower()
    text_tokens = word_tokenize(title_txt)
    text_tokens_stemmed = [stemmer.stem(token) for token in text_tokens]
    snippet_txt = " ".join(text_tokens_stemmed)
    df.at[i,'Title'] = title_txt
    df.at[i,'Snippet'] = snippet_txt
    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql(name='test_cleaned',con=connection)
        connection.commit()

print()
