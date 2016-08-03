# locabike

REST API server based on peewee python module for ORM. API works with json objects.

Simple API routes so far:

../AddReport   
# creates a new stolen bicycle report (TODO: simple datatypes implemented so far, not photo, map location, or date stolen)

../List
# Lists reported stolen bicycles 

../ListAll
# Lists all reported bicycles, including those marked as Found

../ReportSighting
# Report a sighting of a bicycle, this is linked to a reported stolen bicycle.


Example cURL requests:

# AddReport
curl -i -H "Content-Type: application/json" -X POST -d '{"brand":"hybrid bike", "serial_no": "hfjhj23sfdsf", "description": "description of bike", "colour":"black", "owner_contact":"086123456", "locked": "True", "long": "3423.11", "lat": "56556.2", "photo": "http://www.google.ie"}' http://localhost:5000/AddReport

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 208
Server: Werkzeug/0.11.10 Python/2.7.6
Date: Wed, 03 Aug 2016 14:09:56 GMT

{"owner_contact": "086123456", "locked": "True", "description": "description of bike", "map_lat": "56556.2", "photo": "http://www.google.ie", "colour": "black", "serial_no": "hfjhj23sfdsf", "bicycle_id": 2, "found": false, "map_long": "3423.11", "make": "hybrid bike", "date_stolen": ""}

# ReportSighting
curl -i -H "Content-Type: application/json" -X POST -d '{"bicycle_id":"2", "long": "1443.0", "lat": "33454.45", "description": "found abandonedon side of street", "viewers_contact":"086123456"}' http://localhost:5000/ReportSighting

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 366
Server: Werkzeug/0.11.10 Python/2.7.6
Date: Wed, 03 Aug 2016 14:10:18 GMT

{"bicycle": {"owner_contact": "086123456", "locked": true, "description": "description of bike", "map_lat": null, "photo": "http://www.google.ie", "colour": "black", "serial_no": "hfjhj23sfdsf", "bicycle_id": 2, "found": false, "map_long": null, "make": "hybrid bike", "date_stolen": ""}, "description": "found abandonedon side of street", "viewers_contact": "086123456", "map_lat": "33454.45", "date_seen": "", "map_long": "1443.0", "id": 3}

# List
curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/List
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 217
Server: Werkzeug/0.11.10 Python/2.7.6
Date: Wed, 03 Aug 2016 14:22:46 GMT

[{"Bicycle": {"owner_contact": "086123456", "locked": true, "description": "description of bike", "colour": "black", "serial_no": "1234sfdsf", "bicycle_id": 1, "found": false, "make": "mountain bike", "date_stolen": ""}}]

# List All
curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/ListAll
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 217
Server: Werkzeug/0.11.10 Python/2.7.6
Date: Wed, 03 Aug 2016 14:22:46 GMT

[{"mpn": {"owner_contact": "086123456", "locked": true, "description": "description of bike", "colour": "black", "serial_no": "1234sfdsf", "bicycle_id": 1, "found": false, "make": "mountain bike", "date_stolen": ""}}]

# Delete Report
curl -i -H "Content-Type: application/json" -X POST -d '{"bicycle_id":"1"}' http://localhost:5000/DeleteReport
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 20
Server: Werkzeug/0.11.10 Python/2.7.6
Date: Wed, 03 Aug 2016 17:32:38 GMT

successfully deleted

# View Stolen Report
curl -i -H "Content-Type: application/json" -X GET -d '{"bicycle_id":"1"}' http://localhost:5000/ViewStolenReport
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 275
Server: Werkzeug/0.11.10 Python/2.7.6
Date: Wed, 03 Aug 2016 17:45:39 GMT
 
{"owner_contact": "086123456", "locked": true, "description": "description of bike", "map_lat": null, "photo": "http://www.google.ie", "colour": "black", "serial_no": "hfjhj23sfdsf", "bicycle_id": 1, "found": false, "map_long": null, "make": "hybrid bike", "date_stolen": ""}
