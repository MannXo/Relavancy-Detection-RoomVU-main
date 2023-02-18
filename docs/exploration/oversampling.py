from db_utils import DbUtils
import pandas as pd
import numpy as np
import spacy
from spacy import displacy
from sklearn.feature_extraction.text import TfidfTransformer
from spacy.util import minibatch, compounding
from imblearn.over_sampling import SMOTE
from random import randint
from nltk.corpus import wordnet
import nltk


db_utils = DbUtils()
nltk.download('wordnet')

# df = pd.read_csv( "train_cleaned_v2.tsv","r", encoding="utf-8", delimiter='\t')
df_0 = pd.DataFrame(db_utils.get_data_cond(related=0), columns=["indxt", "unnamed","Title", "URL", "Author", "Snippet", "Related"])
df_1 = pd.DataFrame(db_utils.get_data_cond(related=1), columns=["indxt", "unnamed","Title", "URL", "Author", "Snippet", "Related"])
new_df = pd.DataFrame(columns=["indxt", "unnamed","Title", "URL", "Author", "Snippet", "Related"])
for _,row in df_1.iterrows():
    duplicated_rows_rnd = randint(4,6)
    for i in range(duplicated_rows_rnd):
        tmp_row = row
        masked_words_rnd = randint(1,len(tmp_row['Title'].split()))
        for j in range(masked_words_rnd):
            words_index_rnd = randint(1,len(tmp_row['Title'].split()) - 1)
            word = tmp_row['Title'].split()[words_index_rnd]
            synset = wordnet.synsets(word)
            if (len(synset) ==0 ):
                continue
            tmp_row['Title'].replace(word,synset[0].lemmas()[0].name())
        new_df=new_df.append(tmp_row, ignore_index=True)

print()
