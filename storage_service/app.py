#!flask/bin/python
from flask import Flask, request
import Bike 
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/AddReport', methods=['POST'])
def createStolenReport():
    if not request.json or not 'owner_contact' in request.json:
        abort(400)
    bicycle = {
        'make': request.json['make'],
        'serial_no': request.json.get('serial_no', ""),
        'description': request.json.get('description', ""),
        'colour': request.json.get('colour', ""),
        'owner_contact': request.json.get('owner_contact', ""),
        'locked': request.json['locked'],
        'date_stolen': request.json.get('date_stolen', ""),
        'found': False
    }
    return Bike.create_stolenRecord(bicycle)

@app.route('/ReportSighting', methods=['POST'])
def createBicycleSighting():
    if not request.json or not 'viewers_contact' in request.json:
        abort(400)
    bicycle_sighting = {
        'bicycle': request.json['bicycle_id'],
        'location': request.json.get('location', ""),
        'description': request.json.get('description', ""),
        'viewers_contact': request.json.get('viewers_contact', ""),
        'date_seen': request.json.get('date_seen', "")
    }
    return Bike.report_Finding(bicycle_sighting)


@app.route('/List')
def listReports():
    #stolenList = Bike.listReports()
    return Bike.listReports()

@app.route('/ListAll')
def listAllReports():
    #stolenList = Bike.listReports()
    return Bike.listAllReports()
    

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

port = int(os.getenv("PORT", 9000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
