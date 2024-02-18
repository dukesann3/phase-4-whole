#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Employee, Project, Assignment, ProjectChangeLog, AssignmentChangeLog
from datetime import datetime, date

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
        
class EmployeeID(Resource):

    def get(self, id):
        employee = Employee.query.filter_by(id=id).first().to_dict()
        if employee:
            return make_response(employee, 200)
        else:
            return make_response({"message": f"Error, could not find employee with ID: {id}"})
        

class Projects(Resource):

    def get(self):
        all_projects = [project.to_dict(rules=('-assignments',)) for project in Project.query.all()]
        return make_response(all_projects, 200)
    
    def post(self):
        response = request.get_json()
        date_format = "%Y-%m-%d"

        try:
            new_project = Project(
                sales_order=response["sales_order"],
                name=response["name"],
                start_date=datetime.strptime(response["start_date"], date_format).date(),
                expected_end_date=datetime.strptime(response["expected_end_date"], date_format).date(),
                customer_name=response["customer_name"],
                sale_price=response["sale_price"],
                comment=response["comment"]
            )

            db.session.add(new_project)
            db.session.commit()

            return make_response(new_project.to_dict(), 201)
        except:
            return make_response({"message": "Error, could not create new project"}, 401)
    

class ProjectID(Resource):

    def get(self, id):
        project = Project.query.filter_by(id=id).first().to_dict()
        if project:
            return make_response(project, 200)
        else:
            return make_response({"message": f"Error, could not find project with ID: {id}"})
        
    def patch(self, id):
        response = request.get_json()

        try:
            project = Project.query.filter_by(id=id).first()
            for attr in response:
                value = response[attr]
                if attr == "start_date" or attr == "expected_end_date":
                    date_format = "%Y-%m-%d"
                    value = datetime.strptime(value, date_format).date()
                elif attr == "assignments":
                    continue
                
                print(attr)
                setattr(project, attr, value)

            db.session.add(project)
            db.session.commit()

            return make_response(project.to_dict(), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not update project"}, 400)


    def delete(self, id):
        pass
        

class AssignmentInProject(Resource):

    def get(self, prj_id):
        all_assignments_in_project = [assignment.to_dict() for assignment in Assignment.query.filter(Assignment.project_id==prj_id).all()]
        return make_response(all_assignments_in_project.to_dict(), 200)

    
class Assignments(Resource):

    def get(self):
        all_assignments = [assignment.to_dict(rules=('-employee','-project')) for assignment in Assignment.query.all()]
        return make_response(all_assignments, 200)
    
    def post(self):
        response = request.get_json()
        date_format = "%Y-%m-%d"

        try: 
            new_assignment = Assignment(
                employee_id=response["employee_id"],
                project_id=response["project_id"],
                name=response["name"],
                comments=response["comments"],
                start_date=datetime.strptime(response["start_date"], date_format).date(),
                expected_end_date=datetime.strptime(response["expected_end_date"], date_format).date()
            )

            db.session.add(new_assignment)
            db.session.commit()

            return make_response(new_assignment.to_dict(), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not create assignment"}, 400)
    

class AssignmentID(Resource):

    def get(self, id):
        assignment = Assignment.query.filter_by(id=id).first().to_dict()
        if assignment:
            return make_response(assignment, 200)
        else:
            return make_response({"message": f"Error. Could not find assignment with ID: {id}"})
        
    def patch(self, id):
        response = request.get_json()
        date_format = "%Y-%m-%d"

        try:
            assignment = Assignment.query.filter_by(id=id).first()

            for attr in response:
                value = response[attr]
                if attr == "start_date" or attr == "expected_end_date":
                    value = datetime.strptime(response[attr], date_format).date()

                setattr(assignment, attr, value)
            
            db.session.add(assignment)
            db.session.commit()

            return make_response(assignment.to_dict(), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not patch assignment"}, 400)

    def delete(self, id):
        try:
            assignment_to_delete = Assignment.query.filter_by(id=id).first()

            db.session.delete(assignment_to_delete)
            db.session.commit()

            return make_response({}, 200)
        except:
            return make_response({"message": "Error, could not delete assignment"})
        
class ProjectChangeLogs(Resource):

    def get(self):
        print(ProjectChangeLog.query.first())
        #print(ProjectChangeLog.query.first().to_dict(rules=("-project",)))

        all_log = [log.to_dict(rules=("-project",)) for log in ProjectChangeLog.query.all()]
        return make_response(all_log, 200)

    def post(self):
        response = request.get_json()

        try:
            new_log = ProjectChangeLog(
                project_id=response["project_id"],
                detail=response["detail"]
            )

            db.session.add(new_log)
            db.session.commit()

            return make_response(new_log.to_dict(rules=("-project",)), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not create new log"}, 400)
        

class AssignmentChangeLogs(Resource):

    def get(self):
        all_log = [log.to_dict(rules=("-assignment",)) for log in AssignmentChangeLog.query.all()]
        return make_response(all_log, 200)

    def post(self):
        response = request.get_json()

        try:
            new_log = AssignmentChangeLog(
                assignment_id=response["assignment_id"],
                detail=response["detail"]
            )

            db.session.add(new_log)
            db.session.commit()

            return make_response(new_log.to_dict(rules=("-assignment",)), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not create new log"})
        


api.add_resource(Employees, '/employees')
api.add_resource(EmployeeID, '/employees/<int:id>')
api.add_resource(Projects, '/projects')
api.add_resource(ProjectID, '/projects/<int:id>')
api.add_resource(AssignmentInProject, '/projects/assignments/<int:prj_id>')
api.add_resource(Assignments, '/assignments')
api.add_resource(AssignmentID, '/assignments/<int:id>')
api.add_resource(ProjectChangeLogs, '/project_log')
api.add_resource(AssignmentChangeLogs, '/assignment_log')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
