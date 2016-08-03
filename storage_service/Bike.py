import datetime
import sqlite3
import peewee
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import json

db = SqliteDatabase('bicycles.db')
#myDB = pw.MySQLDatabase("mydb", host="mydb.crhauek3cxfw.us-west-2.rds.amazonaws.com", port=3306, user="user", passwd="password")

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

def viewStolenReport(bicycle_id):
    bicycle = Bicycle.get(Bicycle.bicycle_id == bicycle_id)
    return json.dumps(model_to_dict(bicycle), default=date_handler)

def deleteStolenReport(bicycle_id):
    bicycle = Bicycle.get(Bicycle.bicycle_id == bicycle_id)
    bicycle.delete_instance()

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
