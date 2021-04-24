from gensim.parsing import PorterStemmer
global_stemmer = PorterStemmer()

import nltk
import re


def tokenize_text(text, stopwords, stemming=False):

    '''
    :param text: input text
    :param stopwords: list of stopwords to be filtered from text
    :param stemming: booklean, using stemming or not
    :return: list of tokens from the input text - token representation of the input text
    '''

    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

    spec_symbs = ['+', ':', '|', '/', '.', ',']
    tokens_ = []

    for token in tokens:

        token = ''.join(symb for symb in token if symb not in spec_symbs)

        if re.search('[%0-9a-zA-Zа-яА-Я]', token) and token.find('.') == -1 and re.search('-', token) is None:
            tokens_.append(token.lower())

        elif re.search('-', token):
            for tok in token.split('-'):
                tokens_.append(tok.lower())

    if stemming:
        stemmed = [global_stemmer.stem(t) for t in tokens_]
    else:
        stemmed = tokens_

    tokens_out = []
    for token in stemmed:
        if token not in stopwords:
            tokens_out.append(token)

    return tokens_out