from flask import Flask, request, jsonify  
from ImplementationsForTesting import cosine_with_DBSCAN, BERT_with_kmeans, BERT_with_agglomerative, DBSCAN_then_BERT_KNN, DBSCAN_then_BERT_SVM  

app = Flask(__name__)             

@app.route("/run_cosine_with_DBSCAN")               
def run_cosine_with_DBSCAN(): 
    data = request.json
    corpus = data["corpus"]
    clusters = cosine_with_DBSCAN(corpus)                  
    return jsonify(clusters) 

@app.route("/run_BERT_with_kmeans")               
def run_BERT_with_kmeans(): 
    data = request.json
    corpus = data["corpus"]
    clusters = BERT_with_kmeans(corpus)                  
    return jsonify(clusters) 

@app.route("/run_BERT_with_agglomerative")               
def run_BERT_with_agglomerative(): 
    data = request.json
    corpus = data["corpus"]
    clusters = BERT_with_agglomerative(corpus)                  
    return jsonify(clusters) 

@app.route("/run_DBSCAN_then_BERT_KNN")               
def run_DBSCAN_then_BERT_KNN(): 
    data = request.json
    corpus = data["corpus"]
    clusters = DBSCAN_then_BERT_KNN(corpus)                  
    return jsonify(clusters) 

@app.route("/run_DBSCAN_then_BERT_SVM")               
def run_DBSCAN_then_BERT_SVM(): 
    data = request.json
    corpus = data["corpus"]
    clusters = DBSCAN_then_BERT_SVM(corpus)                  
    return jsonify(clusters) 


if __name__ == "__main__":        
    app.run()                     
