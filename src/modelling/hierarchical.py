from sklearn.cluster import AgglomerativeClustering


def cluster(vector_list,num_c):
    hac = AgglomerativeClustering(n_clusters=num_c , affinity = "euclidean")

    hac.fit(vector_list)

    return hac.labels_


    
