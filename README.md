# DATA STORIES

The development of the backend of Data Stories

## API examples

http://localhost:5000/create_new

http://localhost:5000/delete?ds=6a4a58a2-8777-4cbe-896c-85049a928768

http://localhost:5000/get_item?ds=6a4a58a2-8777-4cbe-896c-85049a928768

http://localhost:5000/get_data_stories

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

    curl  -F "file=@test.mp3;type=audio/mp3" -F uuid=c568ba14-a92f-47e2-b98f-9923d93a80b1 localhost:5000/upload

