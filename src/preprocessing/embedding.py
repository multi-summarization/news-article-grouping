import pandas as pd
import numpy as np
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

from .tokenizer import tokenize_text

from keras.preprocessing import sequence

def open_glove_model(file_name):
    embeddings_dict = {}
    with open(file_name, 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector

    return embeddings_dict


def vectorize_text_embedding(df, maxlen=50, lang_model='Glove', text='full', mode='fast'):
    if text == 'full':
        df['full'] = df.title + " " + df.text

    if mode == 'fast':
            df['full_50'] = pd.Series(index=df.index)
            for i, row in df.iterrows():
                curr_word_lst = df['full'][i].split(' ')
                if len(curr_word_lst) > maxlen:
                    df['full_50'][i] = ' '.join(curr_word_lst[:maxlen])
                else:
                    df['full_50'][i] = df['full'][i]

    df_final = df.reset_index(drop=True)


    stopws = stopwords.words('english')


    if lang_model == 'Glove':
        lang_model_semantic = open_glove_model(file_name='model/glove/glove.6B.100d.txt')


    lang_model_sem_dim = len(lang_model_semantic['.'])

    X = []

    for index, row in df_final.iterrows():

        if text == 'full':
            if mode == 'fast':
                curr_descr = df_final['full_50'][index].lower()
            else:
                curr_descr = df_final['text_full'][index].lower()
        elif text == 'title':
            curr_descr = df_final['title'][index].lower()
        elif text == 'text':
            curr_descr = df_final['text'][index].lower()

        #curr_word_tokens = word_tokenize(curr_descr)
        #curr_word_tokens = tokenize_text(curr_word_tokens, stopws)

        curr_word_tokens = tokenize_text(curr_descr, stopws)

        entity_vector_sem = []
        for w in curr_word_tokens:

            if w in lang_model_semantic:
                entity_vector_sem.append(lang_model_semantic[w])
            else:
                entity_vector_sem.append(np.zeros(lang_model_sem_dim))

        X.append(entity_vector_sem)

    # # saving resulting np.array to pickle
    # with open('output/X_Glove.pkl', 'wb') as f:
    #     pickle.dump(X, f)

    X = list(sequence.pad_sequences(X, maxlen=maxlen))
    X = np.array(X)
    print('X.shape', X.shape)

    return X
    
