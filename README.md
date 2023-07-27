# DATA STORIES

The `backend` of Data Stories

## API examples, exchange de UID's by the one u create

New data story:

http://localhost:5000/create_new

Delete data story:

http://localhost:5000/delete?ds=<uuid>

Get a data story:

http://localhost:5000/get_item?ds=<uuid>

List of all data stories:

http://localhost:5000/get_data_stories

Obtain media:

http://localhost:5000/<uuid>/images/<imageName.ext>

http://localhost:5000/<uuid>/video/<videoName.ext>

http://localhost:5000/<uuid>/audio/<audioName.ext>



### Upload files with webform

Open `test.html` adapt the uuid in the hidden field. Use it.


### Upload files test with Postman


http://localhost:5000/upload

POST 

Two conventions:
- the name of the upload field `file` 
- hidden field `uuid` with value of the uuid of the datastoy

![Postman example](postman.png)


### Upload files with Curl

    curl  -F "file=@<name.ext>;type=<mimetype>" -F uuid=<uuid> localhost:5000/upload

 
Example:

    curl  -F "file=@test.mp3;type=audio/mp3" -F uuid=<uuid> localhost:5000/upload

