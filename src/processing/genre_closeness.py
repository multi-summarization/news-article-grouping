from scipy.spatial import distance
from src.processing.vectorize import Vectorize

class GenreCalc:
    def __init__(self,genres_names):
        self.genre_names = genres_names
        self.genre_vectors = [Vectorize.bert_encoding(genre) for genre in genres_names]

    def closest_genre(self,new_genre):
        new_vec = Vectorize.bert_encoding(new_genre)
        closest_genre_id = -2
        cos_val = -2
        for i in range(len(self.genre_vectors)):
            temp = distance.cosine(self.genre_vectors[i],new_vec)
            if temp>cos_val:
                cos_val = temp
                closest_genre_id = i

        return self.genre_names[closest_genre_id]



