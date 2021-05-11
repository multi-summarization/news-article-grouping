from .tokenizer import tokenize_text
from nltk.corpus import stopwords 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline

import nltk
nltk.download('stopwords')
nltk.download('punkt')

def vectorize_texts_tf_idf(data_set, ngram, using_stemming=True):

    '''
    :param data_set: list of texts
    :param ngram: ngram range used
    :param using_stemming: boolean
    :return: X - matrix of texts embeddings
    '''

    stopws = stopwords.words('english')

    corpus = []
    for text in data_set:
        tokens = tokenize_text(text, stopws, using_stemming)
        text_string = ''
        for word in tokens:
                text_string += word + ' '
        corpus.append(text_string)

    vectorizer = TfidfVectorizer(input='content', encoding='utf-8', analyzer='word', max_df=0.4, max_features=20000, min_df=0.00001, use_idf=True, ngram_range=ngram)
    #t0 = time.time()
    X0 = vectorizer.fit_transform(corpus)
    #print("vectorization done in", (time.time() - t0))
    print("n_samples: %d, n_features: %d" % X0.shape)

    if X0.shape[1] > 50:
        svd_flag = 1
        if X0.shape[1] >= 1000:
            n_components_real = 1000
    else:
        svd_flag = 0

    if svd_flag == 1:
        #t0 = time.time()
        normalizer = Normalizer(copy=False)
        svd = TruncatedSVD(n_components=n_components_real, algorithm='randomized', n_iter=5, random_state=None, tol=0.0)
        lsa = make_pipeline(svd, normalizer)  
        X = lsa.fit_transform(X0)
        #print("svd done in: ", time.time() - t0)
    else:
        X = X0

    return X