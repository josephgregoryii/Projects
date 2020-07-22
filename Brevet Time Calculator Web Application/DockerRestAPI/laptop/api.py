#Laptop Service
import os
import csv

#flask imports
from flask import Flask, request, make_response
from flask_restful import Resource, Api

#db import
import pymongo
from pymongo import MongoClient

#create new cleared client
client = MongoClient('db',27017)
#client = MongoClient()
db = client.tododb

# Instantiate the app
app = Flask(__name__)
api = Api(app)

class Laptop(Resource):
    
    def get(self):

        return {
            'Laptops': ['Mac OS', 'Dell', 
            'Windozzee',
	    'Yet another laptop!',
	    'Yet yet another laptop!'
            ]
        }

class listAll(Resource): #listAll return all open and close times in db
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        otime_lst = [item['otime'] for item in items] #adds 'otime' of item into otime_list
        result['otime'] = otime_lst

        ctime_lst = [ item['ctime'] for item in items] #adds 'ctime' of item into ctime_list
        result['ctime'] = ctime_lst

        return result 

class listOpen(Resource):
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        otime_lst = [item['otime'] for item in items] #adds 'otime' of item into otime_list
        result['otime'] = otime_lst

        return result

class listClose(Resource):
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        ctime_lst = [item['ctime'] for item in items] #adds 'otime' of item into otime_list
        result['ctime'] = ctime_lst

        return result

class listAllCSV(Resource):
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]

        csv_output = ""
        
        for item in items:
            csv_output += item['otime'] + ", "
            csv_output += item['ctime'] + ", "

        
        return csv_output[:-2]
        
class listOpenCSV(Resource):
    def get(self):
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]

        csv_output = ""
        for item in items:
            csv_output += item['otime'] + ", "

        return csv_output[:-2]



class listCloseCSV(Resource):
    def get(self):

        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        csv_output = ""
        for item in items:
            csv_output += item['ctime'] + ", "

        return csv_output[:-2]


class listAllJSON(Resource): #listAll return all open and close times in db with json
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        otime_lst = [item['otime'] for item in items] #adds 'otime' of item into otime_list
        result['otime'] = otime_lst

        ctime_lst = [ item['ctime'] for item in items] #adds 'ctime' of item into ctime_list
        result['ctime'] = ctime_lst

        return result

class listOpenJSON(Resource):
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        otime_lst = [item['otime'] for item in items] #adds 'otime' of item into otime_list
        result['otime'] = otime_lst

        return result

class listCloseJSON(Resource):
    def get(self):

        result = {}
        limit = 20
        top = request.args.get('top', 0, type=int)
        if top is not 0: #check to see if top is 0, otherwise set to default value (limit)
            limit = top

        _items = db.tododb.find()
        _items = _items.sort([('otime',pymongo.ASCENDING), ('ctime', pymongo.ASCENDING)]).limit(int(limit))
        items = [item for item in _items]


        ctime_lst = [item['ctime'] for item in items] #adds 'otime' of item into otime_list
        result['ctime'] = ctime_lst

        return result



# Create routes
# Another way, without decorators
api.add_resource(Laptop, '/')

api.add_resource(listAll, "/listAll")
api.add_resource(listOpen, '/listOpenOnly')
api.add_resource(listClose, '/listCloseOnly')

api.add_resource(listAllCSV, '/listAll/csv')
api.add_resource(listOpenCSV, '/listOpenOnly/csv')
api.add_resource(listCloseCSV,'/listCloseOnly/csv')

api.add_resource(listAllJSON, '/listAll/json')
api.add_resource(listOpenJSON, '/listOpenOnly/json')
api.add_resource(listCloseJSON, '/listCloseOnly/json')

api.init_app(app)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
