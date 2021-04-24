from sklearn.neighbors import BallTree, KDTree


def init_tree(embs, treetype='ball'):

    '''
    initalise a KD/Ball tree from the embedding vectors
    :param embs, treetype: embedding vectors of texts, the type of tree to build
    :return: a tree strcuture
    '''

    if treetype == 'ball':
        tree = BallTree(embs, leaf_size=40, metric='euclidean')
    elif treetype == 'kd':
        tree = KDTree(embs, leaf_size=40, metric='euclidean')  # “euclidean”, “chebyshev”, wminkowski, seuclidean, mahalanobis

    return tree