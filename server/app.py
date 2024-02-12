#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Employee

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Employees(Resource):
    
    def get(self):
        all_employees = [employee.to_dict() for employee in Employee.query.all()]
        return make_response(all_employees, 200)
    


api.add_resource(Employees, '/employees')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
