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
    credentials = services['mysql-dev'][0]['credentials']
    db = peewee.MySQLDatabase(credentials['database'], host=credentials['host'], port=int(credentials['port']), user=credentials['user'], passwd=credentials['password'])

class Bicycle(peewee.Model):
    bicycle_id = peewee.PrimaryKeyField()
    make = peewee.CharField()
    serial_no = peewee.TextField()
    description = peewee.TextField()
    colour = peewee.TextField()
    owner_contact = peewee.TextField()
    locked = peewee.BooleanField(default=False)
    date_stolen = peewee.DateTimeField()
    found = peewee.BooleanField(default=False)
    class Meta:
        database = db

class BicycleSighting(peewee.Model):
    bicycle = ForeignKeyField(Bicycle, to_field="bicycle_id")
    location = peewee.TextField()
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

def listReports():
    stolen_list = []
    for bicycle in Bicycle.filter(found=False):
        stolen_list.append(model_to_dict(bicycle))
    print stolen_list
    return json.dumps([dict(mpn=pn) for pn in stolen_list], default=date_handler)

def listAllReports():
    list = []
    for bicycle in Bicycle.select():
        list.append(model_to_dict(bicycle))
    #print list
    return json.dumps([dict(mpn=pn) for pn in list], default=date_handler)
