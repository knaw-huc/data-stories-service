import sqlite3 as sl
import json
import os
import shutil
import uuid

def createDataFolder():
    data = 'data/'
    if not os.path.exists(data):
        os.makedirs(data)
    return True    

def createDataStoriesDB():
    data = 'data'
    # if not os.path.exists(data):
    #     os.makedirs(data)

    con = sl.connect(data + '/datastories.db')
    cur = con.cursor()   
    cur.execute("""
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                uuid TEXT,
                status TEXT,
                owner TEXT,
                filename TEXT,
                created TEXT,
                modified TEXT,
                store TEXT,
                title TEXT,
                groep TEXT
            );
        """) 
    con.commit()


def getDataStoriesDB():
    data = 'data'
    con = sl.connect(data + '/datastories.db')
    cur = con.cursor()   
    sql = "SELECT * FROM stories"
    cur.execute(sql)
    names = list(map(lambda x: x[0], cur.description)) # ergens opgezocht
    print('names', names)
    result = cur.fetchall()
    print('result', result)
    struct = []
    for x in result:
        # print('x', x[1])
        # id = x[1]
        # structure.append({'uuid': id})
        row = {}
        # namen in het resultaat plakken y is een rangnummer in de namenlijst
        for y in range(0, len(names)):
            key = names[y]
            value = x[y]
            row[key] = value
            # s.append({key: value})
            
        struct.append(row)
    print('struct', struct)
    return struct


def getListUUIDs():
    data = 'data'
    con = sl.connect(data + '/datastories.db')
    cur = con.cursor()   
    sql = "SELECT uuid FROM stories"
    cur.execute(sql)
    result = cur.fetchall() # list of tuples
    res = [ele[0] for ele in result] # list comprehension 
    print('result', res)
    
    return list(res)



def tooManyStories(max):
    data = 'data/'
 
    count = len(os.listdir(data))
    print('aantal dirs', count)
    if(count > max):
        return True
    else:
        return False

def getNewId():
    # maakt gebruik van een sql lite database voor gegarandeerde oplopende unieke ids 
    datadir = 'data'
    ideetje = str(uuid.uuid4()) # kan misschien ook als database functie
    # print('ideetje', ideetje)
    con = sl.connect(datadir + '/datastories.db')
    cur = con.cursor()   
    sql = 'INSERT INTO stories (status, uuid) values(?, ?)'
    value = ('x', ideetje)        
    cur.execute(sql, value)
    con.commit()
    # id = con.lastrowid #werkt niet bij deze
    res = cur.execute("SELECT last_insert_rowid()")
    con.commit()
    id = res.fetchone()
    unique_id = id[0]
    sql = 'SELECT id, uuid FROM stories WHERE id = ? '
    value = [unique_id]        
    cur.execute(sql, value)
    con.commit()
    result = res.fetchall()
    # print('result', result)
    return result[0][1]

def createDataStoryFolder(id):
    # misschien ook een eens hiernaar kijken https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories
    # os.path kan wel eens misgaan begrijp ik
    data = 'data/'
    createDataFolder()
    directory = data + str(id)
    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(directory + '/resources/images/')
        os.makedirs(directory + '/resources/audio/')
        os.makedirs(directory + '/resources/video/')

    return True

def deleteDataStoryFolder(uuid):
    data = 'data/'
    directory = data + str(uuid)
    if os.path.exists(directory):
        # os.removedir
        shutil.rmtree(directory)
        return True
    else:
        return False    
    

def removeFromDB(uuid):
    con = sl.connect('data/datastories.db')
    cur = con.cursor()
    sql = 'DELETE FROM stories WHERE uuid = ?'
    cur.execute(sql, (uuid,))
    con.commit()
    return True



def fs_tree_to_dict(path_):
    file_token = ''
    for root, dirs, files in os.walk(path_):
        tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
        tree.update({f: file_token for f in files})
        return tree  # note we discontinue iteration trough os.walk

# https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
# Mikaelblomkvistsson's antwoord bijna onderaan, dit is de meest flexibele m.i. maar ik snap hem niet echt, nu geen tijd



def getDataStory(uuid):
    data = 'data/'
    directory = data + str(uuid) # misschien niet meer nodig
    filename = directory + '/datastory.json'
    # print(filename)
    datastory = {}
    if os.path.exists(filename):
        with open(filename) as json_file:
            datastory = json.load(json_file)
    return datastory
