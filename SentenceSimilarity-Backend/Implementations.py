from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn import svm

from HelperFunctions import get_cluster_dict, cluster_by_index, embed_corpus, re_index_clusters
from KNN import classify_outliers

"""
ClusterDictionary: keys are integers representing cluster labels, values are lists of integers
                   corresponding to the corpus indecies of the sentences in that cluster
"""

"""
cosine_with_DBSCAN
PARAMS
    corpus: List of sentences (strings)
    eps: Float. Distance threshold for two points to be considered neighbours in DBSCAN algorithm
    min_samples: minimum number of samples to form a cluster
OUTPUT
    List containing ClusterDictionary obtained using calculating cosine similarities between tfidfs
    and clustering with the DBSCAN algorithm
"""


def cosine_with_DBSCAN(corpus, eps=0.6, min_samples=3, output="dict"):
    vectorizer = TfidfVectorizer()
    tfidfs = vectorizer.fit_transform(corpus)

    cluster = DBSCAN(
        eps=eps,
        min_samples=min_samples,
        metric="cosine",
        algorithm="brute"
    )
    cluster.fit_predict(tfidfs)
    cluster_assignment = cluster.labels_

    if output == "list":
        return cluster_assignment
    elif output == "sentences":
        return get_cluster_dict(cluster_assignment, corpus)

    return cluster_by_index(cluster_assignment)