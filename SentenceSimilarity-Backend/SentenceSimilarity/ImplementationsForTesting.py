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
    
    return [cluster_by_index(cluster_assignment)]


"""
BERT_with_kmeans
PARAMS
    corpus: List of sentences (strings)
    k: Int. Number of clusters
OUTPUT
    List containing CluserDictionary obtained using BERT and K Means clustering
"""
def BERT_with_kmeans(corpus, k=10):
    corpus_embeddings = embed_corpus(corpus)

    clustering_model = KMeans(n_clusters=k)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_ 

    return [cluster_by_index(cluster_assignment)]


"""
BERT_with_agglomerative
PARAMS
    corpus: List of sentences (strings)
    k: Int. Number of clusters
OUTPUT
    List containing CluserDictionary obtained using BERT and agglomerative clustering
"""
def BERT_with_agglomerative(corpus, k=10):
    corpus_embeddings = embed_corpus(corpus)
    
    clustering_model= AgglomerativeClustering(n_clusters=k)
    clustering_model.fit(corpus_embeddings)
    cluster_assignment = clustering_model.labels_ 

    return [cluster_by_index(cluster_assignment)]


"""
DBSCAN_then_BERT_KNN
PARAMS
    corpus: List of sentences (strings)
    k: Int. Number of nearest neighbours to be analyzed
OUTPUT
    List containing two CluserDictionaries. The first contains clusters as classified by DBSCAN.
    The second contains the results of clustering the outliers of DBSCAN into the original clusters
    using BERT and the K Nearest Neighbours clustering algorithm
"""
def DBSCAN_then_BERT_KNN(corpus, k=5):
    cluster_assignment = cosine_with_DBSCAN(corpus, output="list")
    clusters = cluster_by_index(cluster_assignment)
    outliers = clusters[-1]

    corpus_embeddings = embed_corpus(corpus)
    outlier_classifications = classify_outliers(cluster_assignment, corpus_embeddings, outliers, k)

    return [clusters, outlier_classifications]


"""
DBSCAN_then_BERT_SVM
PARAMS
    corpus: List of sentences (strings)
OUTPUT
    List containing two CluserDictionaries. The first contains clusters as classified by DBSCAN.
    The second contains the results of clustering the outliers of DBSCAN into the original clusters
    using BERT and the Support Vector Machine clustering algorithm
"""
def DBSCAN_then_BERT_SVM(corpus):
    cluster_assignment = cosine_with_DBSCAN(corpus, output="list")
    corpus_embeddings = embed_corpus(corpus)
    original_clusters = cluster_by_index(cluster_assignment)
    
    non_outlier_assignments = []
    non_outlier_embeddings = []
    for i in range(len(cluster_assignment)):
        if cluster_assignment[i] != -1:
            non_outlier_assignments.append(cluster_assignment[i])
            non_outlier_embeddings.append(corpus_embeddings[i])
    
    clf = svm.SVC()
    clf.fit(non_outlier_embeddings, non_outlier_assignments)

    max_cluster = max(cluster_assignment)
    outlier_classifications = {}
    for i in range(-1, max_cluster + 1):
        outlier_classifications[i] = []
        
    for i in range(len(cluster_assignment)):
        if cluster_assignment[i] == -1:
            cluster = clf.predict([corpus_embeddings[i]])[0]
            outlier_classifications[cluster].append(i)
    
    return [original_clusters, outlier_classifications]

"""
DBSCAN_then_BERT_kmeans
PARAMS
    corpus: List of sentences (strings)
    k: Int. Number of additional clusters
OUTPUT
    List containing two CluserDictionaries. The first contains clusters as classified by DBSCAN.
    The second contains the results of clustering the outliers of DBSCAN into new clusters
    using BERT and the K Means clustering algorithm
"""
def DBSCAN_then_BERT_kmeans(corpus, k=5):
    cluster_assignment = cosine_with_DBSCAN(corpus, output="list")
    clusters = cluster_by_index(cluster_assignment)
    outliers = clusters[-1]
    cluster_sentences = get_cluster_dict(cluster_assignment, corpus)
    outlier_sentences = cluster_sentences[-1]
    
    outliers_embeddings = embed_corpus(outlier_sentences)
    clustering_model = KMeans(n_clusters=k)
    clustering_model.fit(outliers_embeddings)
    outlier_assignment = clustering_model.labels_ 
    
    outlier_clusters = {}
    for i in range(k):
        outlier_clusters[i] = []
    
    
    for i in range(len(outlier_assignment)):
        cluster = outlier_assignment[i]
        index = outliers[i]
        if index == 1:
            print(i)
        outlier_clusters[cluster].append(index)
    
    outlier_clusters_re_indexed = re_index_clusters(outlier_clusters, max(cluster_assignment))

    return [clusters, outlier_clusters_re_indexed]

"""
DBSCAN_then_BERT_agglomerative
PARAMS
    corpus: List of sentences (strings)
    k: Int. Number of additional clusters
OUTPUT
    List containing two CluserDictionaries. The first contains clusters as classified by DBSCAN.
    The second contains the results of clustering the outliers of DBSCAN into new clusters
    using BERT and the Agglomerative clustering algorithm
"""
def DBSCAN_then_BERT_agglomerative(corpus, k=5):
    cluster_assignment = cosine_with_DBSCAN(corpus, output="list")
    clusters = cluster_by_index(cluster_assignment)
    outliers = clusters[-1]
    cluster_sentences = get_cluster_dict(cluster_assignment, corpus)
    outlier_sentences = cluster_sentences[-1]
    
    outliers_embeddings = embed_corpus(outlier_sentences)
    clustering_model= AgglomerativeClustering(n_clusters=k)
    clustering_model.fit(outliers_embeddings)
    outlier_assignment = clustering_model.labels_ 
    
    outlier_clusters = {}
    for i in range(k):
        outlier_clusters[i] = []
    
    
    for i in range(len(outlier_assignment)):
        cluster = outlier_assignment[i]
        index = outliers[i]
        if index == 1:
            print(i)
        outlier_clusters[cluster].append(index)
    
    outlier_clusters_re_indexed = re_index_clusters(outlier_clusters, max(cluster_assignment))

    return [clusters, outlier_clusters_re_indexed]
