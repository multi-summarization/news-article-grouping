from sentence_transformers import SentenceTransformer

class Vectorize:

    def bert_encoding(text):
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        doc_embedding = model.encode([text])

        return doc_embedding

import json

if __name__ == "__main__":
    fname = "data/hindu_articles.json"
    with open(fname,"r") as f:
        hindu_articles = json.load(f)

    print(Vectorize.bert_encoding(hindu_articles[0]["content"]))