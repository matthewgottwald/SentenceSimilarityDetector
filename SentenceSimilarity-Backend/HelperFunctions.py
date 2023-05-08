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

"""
dict_to_list
PARAMS
    dic: Dictionary. Format of the output from get_file_dict
OUTPUT
    List of strings 
    List of the sentences in dic

EXAMPLE
dic = {
    0:{"sentence": "I have a cat", "file": "file1.txt"},
    1:{"sentence": "I like pizza", "file": "file1.txt"},
    2:{"sentence": "I play sports", "file": "file1.txt"},
    3:{"sentence": "I own two cats", "file": "file2.txt"},
    4:{"sentence": "I like sports", "file": "file2.txt"},
    5:{"sentence": "I eat pizza", "file": "file2.txt"},
    6:{"sentence": "I own a cat", "file": "file3.txt"},
    7:{"sentence": "I love pizza", "file": "file3.txt"},
    8:{"sentence": "I like to play sports", "file": "file3.txt"},
    9:{"sentence": "My name is Bob", "file": "file3.txt"}
}

dict_to_list(dic) =>
[
    "I have a cat", "I like pizza", "I play sports",
    "I own two cats", "I like sports", "I eat pizza",
    "I own a cat", "I love pizza", "I like to play sports", "My name is Bob"
]
"""

def dict_to_list(dic):
    ls = []
    for i in range(max(dic.keys()) + 1):
        sentence = dic[i]["sentence"]
        ls.append(sentence)
        
    return ls


"""
cluster_by_index_with_doc
PARAMS
    clusters: Dictionary. Keys are cluster labels. Values are
              lists of integers. The elements of the lists represent
              keys for sentences in sentence_dict
    sentence_dict: Dictionary. Format of the output from get_file_dict
OUTPUT
    Dictionary
    Keys are cluster labels. Values are lists of dictionaries. Each 
    dictionary is a value from sentence_dict such that if its key was in
    a cluster's list then it can be found under that cluster label
EXAMPLE
clusters = {
    -1:[9],
    0:[0, 3, 6],
    1:[1, 5, 7],
    2:[2, 4, 8]
}

sentence_dict = {
    0:{"sentence": "I have a cat", "file": "file1.txt"},
    1:{"sentence": "I like pizza", "file": "file1.txt"},
    2:{"sentence": "I play sports", "file": "file1.txt"},
    3:{"sentence": "I own two cats", "file": "file2.txt"},
    4:{"sentence": "I like sports", "file": "file2.txt"},
    5:{"sentence": "I eat pizza", "file": "file2.txt"},
    6:{"sentence": "I own a cat", "file": "file3.txt"},
    7:{"sentence": "I love pizza", "file": "file3.txt"},
    8:{"sentence": "I like to play sports", "file": "file3.txt"},
    9:{"sentence": "My name is Bob", "file": "file3.txt"}
}

cluster_by_index_with_doc(clusters, sentence_dict) =>
{
    -1:[9:{"sentence": "My name is Bob", "file": "file3.txt"}],
    0:[
        0:{"sentence": "I have a cat", "file": "file1.txt"},
        3:{"sentence": "I own two cats", "file": "file2.txt"},
        6:{"sentence": "I own a cat", "file": "file3.txt"}
    ],
    1:[
        1:{"sentence": "I like pizza", "file": "file1.txt"},
        5:{"sentence": "I eat pizza", "file": "file2.txt"},
        7:{"sentence": "I love pizza", "file": "file3.txt"} 
    ],
    2:[
        2:{"sentence": "I play sports", "file": "file1.txt"},
        4:{"sentence": "I like sports", "file": "file2.txt"},
        8:{"sentence": "I like to play sports", "file": "file3.txt"}
    ]
}
"""
def cluster_by_index_with_doc(clusters, sentence_dict):
    res = {}
    for key in clusters.keys():
        indecies = clusters[key]
        sentences = []
        for j in range(len(indecies)):
            index = indecies[j]
            sentences.append(sentence_dict[index])
        res[key] = sentences
    return res

"""
get_file_dict
PARAMS
    path: String. filepath to folder with all of the files
    files: List of strings. elements are filenames
OUTPUT
    Dictionary
    This is a dictionary where each key/value pair represents a sentence from 
    one of the files.
    The keys are numbers (meant to match the index of each sentence when
    the dictionary is a param in dict_to_list).
    Values are dictionaries, each with two keys: "sentence" and "file".
    Both values are strings. "sentence" is the sentence, and file is the
    name of the file the sentence is from.

EXAMPLE
fileFolder
    file1.txt: I have a cat. I like pizza. I play sports.
    file2.txt: I own two cats. I like sports. I eat pizza.
    file3.txt: I own a cat. I love pizza. I like to play sports. My name is Bob.

get_file_dict("fileFolder/", ["file1.txt", "file2.txt", "file3.txt"]) =>
{
    0:{"sentence": "I have a cat", "file": "file1.txt"},
    1:{"sentence": "I like pizza", "file": "file1.txt"},
    2:{"sentence": "I play sports", "file": "file1.txt"},
    3:{"sentence": "I own two cats", "file": "file2.txt"},
    4:{"sentence": "I like sports", "file": "file2.txt"},
    5:{"sentence": "I eat pizza", "file": "file2.txt"},
    6:{"sentence": "I own a cat", "file": "file3.txt"},
    7:{"sentence": "I love pizza", "file": "file3.txt"},
    8:{"sentence": "I like to play sports", "file": "file3.txt"},
    9:{"sentence": "My name is Bob", "file": "file3.txt"}
}
"""

def get_file_dict(path, files):
    file_dict = {}
    i = 0
    for k in range(len(files)):
        filename = files[k]
        f = open(path + filename, "r")
        text = f.read()
        sentences = text.replace("\n", "").split(".")
        for j in range(len(sentences)):
            sentence = sentences[j]
            if sentence != "":
                file_dict[i] = { "sentence": sentence, "file": filename }
                i+=1
    return file_dict