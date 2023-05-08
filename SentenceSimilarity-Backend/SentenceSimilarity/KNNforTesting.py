from numpy import dot
from math import sqrt 

def get_neighbors(clusters, sentences, outlier, k):
    distances = list()
    for i in range(len(clusters)):
        cluster = clusters[i]
        if cluster != -1:
            sentence = sentences[i]
            dist = sqrt(dot(sentence, sentence) - 2 * dot(sentence, outlier) + dot(outlier, outlier))
            distances.append((cluster, dist))
    distances.sort(key=lambda tup:tup[1])
    neighbors = list()
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors

def predict_classification(clusters, sentences, outlier, k):
    neighbors = get_neighbors(clusters, sentences, outlier, k)
    prediction = max(set(neighbors), key=neighbors.count)
    return prediction


def classify_outliers(clusters, sentences, outliers, k):
    max_cluster = max(clusters)
    classifications = {}
    for i in range(-1, max_cluster + 1):
        classifications[i] = []
        
    for j in outliers:
        prediction = predict_classification(clusters, sentences, sentences[j], k)
        classifications[prediction].append(j)
    
    return classifications