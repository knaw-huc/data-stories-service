from flask import Flask, request, jsonify
import json
from elastic_index import Index
import requests
import random
import sqlite3 as sl
import os

from functions import (
    getNewId, createDataStoryFolder, removeFromDB, 
    deleteDataStoryFolder,getDataStoryStructure, fs_tree_to_dict,
    tooManyStories, createDataFolder, createDataStoriesDB, getDataStoriesDB
)
# https://peps.python.org/pep-0328/#rationale-for-parentheses

app = Flask(__name__)

config = {
    "url" : "localhost",
    "port" : "9200",
    "doc_type" : "ds"
}

index = Index(config)

# wordt maar 1 keer gedaan na het opstarten
@app.before_first_request
def before_first_request():
    # datafolder aanmaken
    print('initialisatie')
    createDataFolder()
    createDataStoriesDB()

    # app.logger.info("before_first_request")



@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Content-type'] = 'application/json'
    return response

@app.route("/")
def hello_world():
    retStruc = {"app": "Data Stories Slurf=", "version": "0.1"}
    return json.dumps(retStruc)

@app.route("/browse")
def browse():
    ret_struc = index.browse()
    return json.dumps(ret_struc)

@app.route("/create_new")
def create_new():
    status = 'OK'
    max = 100 # maximaal 100 datastories
    if tooManyStories(max):
        response = {"status": 'ff aan de rem getrokken'}
        return json.dumps(response)        

    id = getNewId()
    status = createDataStoryFolder(id) # plus sub directories, hoef geen json file aan te maken
    if status == True:
        # stringie = 'I created something new! De unieke id is: ' + str(id)
        response = {"datastory_id": id}
        return json.dumps(response)

@app.route("/delete" , methods=['GET'])
def delete():
    status = 'OK'
    id = request.args.get("ds")
    if deleteDataStoryFolder(id):
        status = 'OK' 
    else: 
        status = 'DATASTORY NOT FOUND'  

    removeFromDB(id) # nog even goed naar kijken of dit nu klopt 
    response = {"status": status}
    return json.dumps(response)

# datastory is de inhoud van de json file, ik hoef geen structuur te parsen
@app.route("/get_item", methods=['GET'] )
def get_item():
    status = ''
    datastory = {}
    uuid = request.args.get("ds")
    if not uuid:
        status = 'INVALID REQUEST'
        datastory = {}
    else:    
        datastory = getDataStoryStructure(uuid)
        if not datastory:
            status = 'DATASTORY NOT FOUND'
            datastory = {}
        else:
            status = 'OK'

    print('ds', datastory)        
    response = {"status": status, "datastory": datastory}
    return json.dumps(response)


# hier moet de sqllite database bevraagd worden, om de lijstpagina te genereren
@app.route("/get_data_stories")
def getDataStories():


    structure = {'message': 'nothing yet'}
    # data = 'data/'
    status = 'OK'
    # structure = fs_tree_to_dict(data)
    # print(structure)
    structure = getDataStoriesDB()

    response = {"status": status, "structure": structure}
    return json.dumps(response)


@app.route("/update_datastory", methods=['POST'])
def updateDataStory():
    return


#Start main program

if __name__ == '__main__':
    app.run()

