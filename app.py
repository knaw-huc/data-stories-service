from flask import Flask, request, jsonify
import json
from elastic_index import Index
import requests
import random
import sqlite3 as sl

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
    retStruc = {"app": "Data Stories slervice", "version": "0.1"}
    return json.dumps(retStruc)

@app.route("/browse")
def browse():
    ret_struc = index.browse()
    return json.dumps(ret_struc)

def getNewId():
    # maakt gebruik van een sql lite database voor gegarandeerde oplopende unieke ids 
    con = sl.connect('datastories.db')
    cur = con.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS counter (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                status TEXT
            );
        """) 
    con.commit()
    sql = 'INSERT INTO counter (status) values(?)'
    data = [('x')]        
    cur.execute(sql, data)
    con.commit()
    # id = con.lastrowid #werkt niet bij deze
    res = cur.execute("SELECT last_insert_rowid()")
    con.commit()
    id = res.fetchone()
    unique_id = id[0]
    return unique_id

@app.route("/create_new")
def create_new():
    id = getNewId()
    stringie = 'I created something new! De unieke 1id is: ' + str(id)
    return json.dumps(stringie)

@app.route("/delete" , methods=['GET'])
def delete():
    id = request.args.get("ds")
    print('I deleted a datastorie whith id:' + id)




#Start main program

if __name__ == '__main__':
    app.run()

