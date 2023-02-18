from db_utils import DbUtils
import pandas as pd
import numpy as np
import spacy
from spacy import displacy
from sklearn.feature_extraction.text import TfidfTransformer
from spacy.util import minibatch, compounding
from imblearn.over_sampling import SMOTE
import random
# import explacy


db_utils = DbUtils()

# df = pd.read_csv( "train_cleaned_v2.tsv","r", encoding="utf-8", delimiter='\t')
df = pd.DataFrame(db_utils.get_data(), columns=["Title", "URL", "Author", "Snippet", "Related"])
spacy_model = spacy.load('en_core_web_sm')

tf = TfidfTransformer()
tf.fit_transform()


# parsed_text_df = spacy_model(df['Snippet'])
text_cat=spacy_model.create_pipe( "textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"})
spacy_model.add_pipe(text_cat, last=True)
text_cat.add_label("Related")
text_cat.add_label("Not Related")

# Converting the dataframe into a list of tuples
df['tuples'] = df.apply(lambda row: (row['Title'],row['Related']), axis=1)
train =df['tuples'].tolist()
def load_data(split=0.8):
    train_data=train
    # Shuffle the data
    random.shuffle(train_data)
    texts, labels = zip(*train_data)
    # get the categories for each review
    cats = [{"Related": bool(y), "Not Related": not bool(y)} for y in labels]

    # Splitting the training and evaluation data
    split = int(len(train_data) * split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

# Calling the load_data() function
n_texts = 10182
(train_texts, train_cats), (dev_texts, dev_cats) = load_data()

# Processing the final format of training data
train_data = list(zip(train_texts,[{'cats': cats} for cats in train_cats]))

def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 0.0 # True positives
    fp = 1e-8 # False positives
    fn = 1e-8 # False negatives
    tn = 0.0 # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        if cats[i][max(doc.cats, key=doc.cats.get)]:
            if max(doc.cats, key=doc.cats.get) == "Related":
                tp+=1.0
            else:
                tn+=1.0
        else:
            if max(doc.cats, key=doc.cats.get) == "Related":
                fp+=1.0
            else:
                fn+=1.0           
    accuracy = (tp + tn) / (fp + fn + tp + tn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"textcat_a": accuracy,"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}

#("Number of training iterations", "n", int))
n_iter=30


# Disabling other components
other_pipes = [pipe for pipe in spacy_model.pipe_names if pipe != 'textcat']
with spacy_model.disable_pipes(*other_pipes): # only train textcat
    optimizer = spacy_model.begin_training()

    print("Training the model...")
    print('{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS','Accuracy', 'Percision', 'Recall', 'F1'))

    # Performing training
    for i in range(n_iter):
        losses = {}
        batches = minibatch(train_data, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            spacy_model.update(texts, annotations, sgd=optimizer, drop=0.2,
            losses=losses)

        # Calling the evaluate() function and printing the scores
        with text_cat.model.use_params(optimizer.averages):
            scores = evaluate(spacy_model.tokenizer, text_cat, dev_texts, dev_cats)
        print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}'
        .format(losses['textcat'], scores['textcat_a'],scores['textcat_p'],
        scores['textcat_r'], scores['textcat_f']))

