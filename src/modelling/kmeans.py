from sklearn.cluster import KMeans


def cluster(vector_list, k_val):
    kmeans = KMeans(n_clusters=k_val, random_state=0)

    kmeans.fit(vector_list)

    return kmeans.labels_


    
