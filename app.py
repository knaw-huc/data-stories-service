from flask import Flask, request, jsonify
import json
from elastic_index import Index
import requests


app = Flask(__name__)

config = {
    "url" : "localhost",
    "port" : "9200",
    "doc_type" : "ds"
}

index = Index(config)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Content-type'] = 'application/json'
    return response

@app.route("/")
def hello_world():
    retStruc = {"app": "Data Stories service", "version": "0.1"}
    return json.dumps(retStruc)

@app.route("/browse")
def browse():
    ret_struc = index.browse()
    return json.dumps(ret_struc)

#Start main program

if __name__ == '__main__':
    app.run()

