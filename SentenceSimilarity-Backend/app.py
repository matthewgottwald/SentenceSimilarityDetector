from flask import Flask, request, jsonify, abort
import os

from Implementations import cosine_with_DBSCAN 
from HelperFunctions import dict_to_list, cluster_by_index_with_doc, get_file_dict

from flask_cors import CORS, cross_origin
UPLOAD_FOLDER = 'TextFiles/'


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'           
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


"""
/find_clusters
POST
    - Request body is a json with key 'filenames' and value is a list of 
      filenames.
    - find_clusters() uses the sentences from the files as input for 
      cosine_with_DBSCAN() which returns a dictionary where the keys are 
      cluster labels and the values are lists of sentence idecies. The 
      clusters are then associated back to the sentences and the filenames in
      a new dictionary which is sent as a response json
"""

@app.route("/find_clusters", methods=["GET","POST"])  
def find_clusters():
    filenames = request.json["filenames"]
    data = get_file_dict(app.config['UPLOAD_FOLDER'], filenames)
    corpus = dict_to_list(data)
    clusters = cosine_with_DBSCAN(corpus) 
    clusters_with_docs = cluster_by_index_with_doc(clusters, data)
    print(clusters_with_docs)
    return jsonify(clusters_with_docs) 


"""
/upload
POST
    - Request body should be a form containing a file to be uploaded.
    - upload() checks if the file is a text file. If it's not a text file,
      aborts with error. If it is a text file, saves the file to the 
      UPLOAD_FOLDER.

GET, DELETE
    - sends response with empty json, doesn't do anything.

Note: This endpoint is meant to be called by filepond, the file uploading
library used in the front end.
"""

@app.route("/upload", methods=["GET","POST", "DELETE"])
@cross_origin()
def upload():
    if request.method in ["GET", "DELETE"] :
        return {}
    file = request.files['filepond']
    filename = file.filename
    content_type = file.content_type
    if "text" in content_type:
        text = file.read().decode("utf-8")
        f = open(app.config['UPLOAD_FOLDER'] + filename, "w")
        f.write(text)
        f.close()
        return {}
    abort(500)

    



if __name__ == "__main__":        
    app.run()   
