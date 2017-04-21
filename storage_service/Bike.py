import datetime
import sqlite3
import peewee
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import os

#db = SqliteDatabase('bicycles.db')
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    from pprint import pprint
    pprint(services)
    credentials = services['mysql-dev'][0]['credentials']
    db = peewee.MySQLDatabase(credentials['database'], host=credentials['host'], port=int(credentials['port']), user=credentials['user'], passwd=credentials['password'])

class Bicycle(peewee.Model):
    bicycle_id = peewee.PrimaryKeyField()
    make = peewee.TextField()
    serial_no = peewee.TextField()
    description = peewee.TextField()
    colour = peewee.TextField()
    owner_contact = peewee.TextField()
    locked = peewee.BooleanField(default=False)
    date_stolen = peewee.DateTimeField()
    photo = peewee.TextField()
    found = peewee.BooleanField(default=False)
    map_long = peewee.DecimalField()
    map_lat = peewee.DecimalField()
    class Meta:
        database = db

class BicycleSighting(peewee.Model):
    bicycle = ForeignKeyField(Bicycle, to_field="bicycle_id")
    map_long = peewee.DecimalField()
    map_lat = peewee.DecimalField()
    description = peewee.TextField()
    date_seen = peewee.DateTimeField()
    viewers_contact = peewee.TextField()
    class Meta:
        database = db
    
#Bicycle.drop_table()
Bicycle.create_table(True)
BicycleSighting.create_table(True)

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()

def create_stolenRecord(bicycle_dict):
    bicycle = dict_to_model(Bicycle, bicycle_dict)
    bicycle.save()
    return json.dumps(model_to_dict(bicycle), default=date_handler)

def update_StolenRecord(bicycle_id, bicycle_dict):
    bicycle = dict_to_model(Bicycle, bicycle_dict)
    bicycle.save()
    return json.dumps(model_to_dict(bicycle), default=date_handler)

def report_Finding(bicycle_sighting_dict):
    bicycle_sighting = dict_to_model(BicycleSighting, bicycle_sighting_dict)
    bicycle_sighting.save()
    return json.dumps(model_to_dict(bicycle_sighting), default=date_handler)

def viewStolenReport(bicycle_id):
    bicycle = Bicycle.get(Bicycle.bicycle_id == bicycle_id)
    return json.dumps(convert_decimals(bicycle), default=date_handler)

def deleteStolenReport(bicycle_id):
    bicycle = Bicycle.get(Bicycle.bicycle_id == bicycle_id)
    bicycle.delete_instance()

def convert_decimals(bicycle):
    d = model_to_dict(bicycle)

    # This is an ugly hack because I'm tired
    d['map_lat'] = float(d['map_lat'])
    d['map_long'] = float(d['map_long'])

    return d

def listReports():
    stolen_list = []
    for bicycle in Bicycle.filter(found=False):
        stolen_list.append(convert_decimals(bicycle))
    return json.dumps([dict(Bicycle=pn) for pn in stolen_list], default=date_handler)

def listAllReports():
    list = []
    for bicycle in Bicycle.select():
        list.append(convert_decimals(bicycle))
    #print list
    return json.dumps([dict(Bicycle=pn) for pn in list], default=date_handler)
