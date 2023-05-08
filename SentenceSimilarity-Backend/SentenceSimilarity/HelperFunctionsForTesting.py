from sentence_transformers import SentenceTransformer

def get_cluster_dict(clusters, sentences):
    max_cluster = max(clusters)
    cluster_dict = {}
    for i in range(-1, max_cluster + 1):
        cluster_dict[i] = []
    
    for i in range(len(clusters)):
        cluster = clusters[i]
        sentence = sentences[i]
        cluster_dict[cluster].append(sentence)
    
    return cluster_dict


def cluster_by_index(clusters):
    max_cluster = max(clusters)
    cluster_dict = {}
    for i in range(-1, max_cluster + 1):
        cluster_dict[i] = []
    
    for i in range(len(clusters)):
        cluster = clusters[i]
        index = i
        cluster_dict[cluster].append(index)
    
    return cluster_dict

"""
embed_corpus
PARAMS
    corpus: List of sentences (strings)
OUTPUT
    List of numpy arrays
    Each array is a vector embedding of a sentence in corpus (indecies preserved)
"""
def embed_corpus(corpus):
    embedder = SentenceTransformer('bert-base-nli-mean-tokens')
    return embedder.encode(corpus)


"""
re_index_clusters
PARAMS
    clusters: ClusterDictionary
    x: Integer. Number that all re-indexed cluster labels must be above
OUTPUT
    clusters with all non-negative keys re-labelled to be above x
"""
def re_index_clusters(clusters, x):
    starting_index = x + 2
    re_indexed = {}

    if -1 in clusters.keys():
        re_indexed[-1] = clusters[-1]

    for key in clusters.keys():
        re_indexed[starting_index + key] = clusters[key]
    
    return re_indexed