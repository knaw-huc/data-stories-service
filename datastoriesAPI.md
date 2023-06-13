API calls voor Data Stories editor


Call:
/create_new

Method:
GET

Request parameters:
Geen

Response:
{"datastory_id": "<datastory_id>"}

---------------------------------------------------------------------- 

Call:
/delete

Method:
GET

Request parameters:
?ds=<datastory_id>

Response:
{"status": "<status>"}

status = "OK" || "DATASTORY NOT FOUND" || "NOT PERMITTED"

---------------------------------------------------------------------- 

Call:
/get_item

Method:
GET

Request parameters:
?ds=<datastory_id>

Response:
{"status": "<status>",
"datastory": {<datastory>} || {}}

status = "OK" || "DATASTORY NOT FOUND" || "NOT PERMITTED"

---------------------------------------------------------------------- 

Call:
/get_data_stories

Method:
GET

Request parameters:
Geen

Response:
In json formaat de data in de sql-lite structuur

---------------------------------------------------------------------- 

Call:
/update_datastory

Method:
POST

Request parameters:
JSON structuur:
{"datastory_id": "<datastory_id>",
"datastory": {<datastory>}}

Response:
{"status": "<status>"}

status = "OK" || "DATASTORY NOT FOUND" || "NOT PERMITTED" || "ERROR"

---------------------------------------------------------------------- 




