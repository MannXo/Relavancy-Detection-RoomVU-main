import random

import pandas as pd
import spacy
from spacy.training.example import Example


class SpacyModel:
    def __init__(self, number_of_training_iterations: int = 100, df: pd.DataFrame = None, batch_testing: bool=False):
        self.number_of_training_iterations = number_of_training_iterations
        if df is None:
            self.df = pd.read_csv(r"C:\Users\Desktop\Desktop\RoomVU Pilot\docs\exploration\tst.tsv", sep='\t', encoding="utf-8")
        else:
            self.df = df
        try:
            self.spacy_model = spacy.load("./en_example_pipeline")
            self.text_cat = self.spacy_model.components[7][1]
        except:

            self.spacy_model = spacy.load('en_core_web_trf')

            self.text_cat = self.spacy_model.add_pipe("textcat", last=True)

            self.text_cat.add_label("Related")
            self.text_cat.add_label("Not Related")

        self.df["tuples"] = self.df.apply(lambda row: (row["Title"], row["Related"]), axis=1)                                                                          
        if batch_testing:
            (self.dev_texts, self.dev_cats) = self.load_data(self.df["tuples"].tolist(), batch_testing)
        else:
            (self.train_texts, self.train_cats), (self.dev_texts, self.dev_cats) = self.load_data(self.df["tuples"].tolist(), batch_testing)
            self.train_data = list(zip(self.train_texts, [{"cats": cats} for cats in self.train_cats]))

    def load_data(self, data:list, batch_testing: bool, split:float=0.8):
        train_data = data
        random.shuffle(train_data)
        texts, labels = zip(*train_data)
        cats = [{"Related": bool(y), "Not Related": not bool(y)} for y in labels]
        if batch_testing:
            return (texts,cats)
        split = int(len(train_data) * split)
        return (texts[:split], cats[:split]), (texts[split:], cats[split:])

    def predict(self, title: str):
        optimizer = self.spacy_model.resume_training()
        with self.text_cat.model.use_params(optimizer.averages):
            doc = (self.spacy_model.tokenizer(title))
            for _, d in enumerate(self.text_cat.pipe([doc])):
                return d.cats

    def batch_evaluate(self):
        return self.evaluate(self.dev_texts, self.dev_cats)

    def evaluate(self, texts, cats):
        docs = (self.spacy_model.tokenizer(text) for text in texts)
        tp = 0.0  # True positives
        fp = 1e-8  # False positives
        fn = 1e-8  # False negatives
        tn = 0.0  # True negatives
        for i, doc in enumerate(self.text_cat.pipe(docs)):
            if cats[i][max(doc.cats, key=doc.cats.get)]:
                if max(doc.cats, key=doc.cats.get) == "Related":
                    tp += 1.0
                else:
                    tn += 1.0
            else:
                if max(doc.cats, key=doc.cats.get) == "Related":
                    fp += 1.0
                else:
                    fn += 1.0
        accuracy = (tp + tn) / (fp + fn + tp + tn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        if (precision + recall) == 0:
            f_score = 0.0
        else:
            f_score = 2 * (precision * recall) / (precision + recall)
        return {"textcat_a": accuracy, "textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}

    def train(self):
        return_values = []
        examples = []
        for x, c in self.train_data:
            doc = self.spacy_model.make_doc(x)
            example = Example.from_dict(doc, c)
            examples.append(example)
        losses = {}
        optimizer = self.spacy_model.resume_training()
        with self.spacy_model.select_pipes(enable="textcat"):
            optimizer = self.spacy_model.create_optimizer()
            print("Training the model...")
            print("{:^5}\t{:^5}\t{:^5}\t{:^5}\t{:^5}".format("LOSS", "Accuracy", "Percision", "Recall", "F1"))
            for itn in range(self.number_of_training_iterations):
                random.shuffle(examples)
                self.spacy_model.update(examples, drop=0.5, losses=losses)
                with self.text_cat.model.use_params(optimizer.averages):
                    scores = self.evaluate(self.dev_texts, self.dev_cats)
                print(
                    "{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}".format(
                        losses["textcat"], scores["textcat_a"], scores["textcat_p"], scores["textcat_r"], scores["textcat_f"]
                    )
                )
                return_values.append([losses["textcat"], scores["textcat_a"], scores["textcat_p"], scores["textcat_r"], scores["textcat_f"]])

        self.spacy_model.to_disk("./en_example_pipeline")
        return return_values