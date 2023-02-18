from langdetect import detect
import pandas as pd
from db_utils import DbUtils
import collections

db_utils = DbUtils()
df = pd.DataFrame(db_utils.get_data(), columns=["Title", "URL", "Author", "Snippet", "Related"])
title_langs = []
snippet_langs = []
for _,row in df.iterrows():
    title_langs.append(detect(row['Title']))
    snippet_langs.append(detect(row['Snippet']))

frequency = collections.Counter(snippet_langs)
print(dict(frequency))
detect("Ein, zwei, drei, vier")