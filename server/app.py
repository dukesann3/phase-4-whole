#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Employee, Project, Assignment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Employees(Resource):
    
    def get(self):
        all_employees = [employee.to_dict(rules=('-assignments',)) for employee in Employee.query.all()]
        return make_response(all_employees, 200)

    def post(self):
        response = request.get_json()

        try:
            new_employee = Employee(
                first_name=response["first_name"],
                last_name=response["last_name"],
                department=response["department"],
                role=response["role"]
            )
            db.session.add(new_employee)
            db.session.commit()

            return make_response(new_employee.to_dict(), 201)
        except:
            return make_response({"message": "Error, could not create new employee"}, 403)


    
class Projects(Resource):

    def get(self):
        all_projects = [project.to_dict(rules=('-assignments',)) for project in Project.query.all()]
        return make_response(all_projects, 200)
    
class Assignments(Resource):

    def get(self):
        all_assignments = [assignment.to_dict(rules=('-employee','-project')) for assignment in Assignment.query.all()]
        return make_response(all_assignments, 200)
    
class AssignmentID(Resource):

    def get(self, id):
        assignment = Assignment.query.filter_by(id=id).first().to_dict()
        if assignment:
            return make_response(assignment, 200)
        else:
            return make_response({"message": f"Error. Could not find assignment with ID: {id}"})


api.add_resource(Employees, '/employees')
api.add_resource(Projects, '/projects')
api.add_resource(Assignments, '/assignments')
api.add_resource(AssignmentID, '/assignments/<int:id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
