#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Employee, Project, Assignment, ProjectChangeLog, AssignmentChangeLog
from datetime import datetime, date
import ipdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Employees(Resource):
    
    def get(self):
        all_employees = [employee.to_dict(rules=('-assignments','-projects')) for employee in Employee.query.all()]
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
            return make_response({"message": "Error, could not create new employee"}, 404)
        
class EmployeeID(Resource):

    def get(self, id):
        try:
            employee = Employee.query.filter(Employee.id==id).first()
            return make_response(employee.to_dict(), 200)
        except:
            return make_response({"error": f"Could not find employee with id: {id}"}, 404)

        

class Projects(Resource):

    def get(self):
        all_projects = [project.to_dict(rules=('-assignments','-project_change_log')) for project in Project.query.all()]
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

            start_date = datetime.strptime(response["start_date"], date_format).date()
            end_date = datetime.strptime(response["expected_end_date"], date_format).date()

            if start_date > end_date:
                raise ValueError
 
            db.session.add(new_project)
            db.session.commit()

            new_prj_log = ProjectChangeLog(
                project_id=new_project.id,
                detail="Initial Project Creation"
            )

            db.session.add(new_prj_log)
            db.session.commit()

            return make_response(new_project.to_dict(), 201)
        except ValueError:
            return make_response({"message": "Error, start date cannot be greater than end date"}, 404)
        except:
            return make_response({"message": "Error, could not create new project"}, 404)
    

class ProjectID(Resource):

    def get(self, id):
        project = Project.query.filter_by(id=id).first()
        if project:
            return make_response(project.to_dict(rules=("employees","-employees.assignments", "-employees.projects")), 200)
        else:
            return make_response({"error": f"Could not find project with id: {id}"}, 404)
        
    def patch(self, id):
        response = request.get_json()
        new_response = {}
        for resp in response:
            if not resp == "assignments" and not resp == "project_change_log":
                new_response[resp] = response[resp]

        try:
            project = Project.query.filter_by(id=id).first()
            for attr in new_response:
                value = new_response[attr]
                if attr == "start_date" or attr == "expected_end_date":
                    date_format = "%Y-%m-%d"
                    value = datetime.strptime(value, date_format).date()
                elif attr == "assignments" or attr == "project_change_log" or attr == "detail":
                    continue
                setattr(project, attr, value)

            db.session.add(project)
            db.session.commit()

            project_log = ProjectChangeLog(
                project_id=project.id,
                detail=response["detail"]
            )

            db.session.add(project_log)
            db.session.commit()

            return make_response(project.to_dict(), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not update project"}, 404)


    def delete(self, id):
        try:
            project_to_delete = Project.query.filter_by(id=id).first()

            new_prj_log = ProjectChangeLog(
                project_id=id,
                detail="Deleted Project"
            )

            db.session.delete(project_to_delete)
            db.session.commit()

            db.session.add(new_prj_log)
            db.session.commit()

            return make_response({}, 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not delete project"}, 404)
        

class AssignmentInProject(Resource):

    def get(self, prj_id):
        all_assignments_in_project = [assignment.to_dict() for assignment in Assignment.query.filter(Assignment.project_id==prj_id).all()]
        return make_response(all_assignments_in_project.to_dict(), 200)

    
class Assignments(Resource):

    def get(self):
        all_assignments = [assignment.to_dict(rules=('-employee','-project', '-assignment_change_log')) for assignment in Assignment.query.all()]
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

            start_date = datetime.strptime(response["start_date"], date_format).date()
            end_date = datetime.strptime(response["expected_end_date"], date_format).date()

            if start_date > end_date:
                raise ValueError

            db.session.add(new_assignment)
            db.session.commit()

            new_asgn_log = AssignmentChangeLog(
                assignment_id=new_assignment.id,
                detail="Initial Assignment Creation"
            )

            db.session.add(new_asgn_log)
            db.session.commit()

            return make_response(new_assignment.to_dict(), 200)
        except ValueError:
            return make_response({"message": "Error, start date cannot be greater than end date"}, 404)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not create new assignment"}, 404)
    

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
                elif attr == "detail":
                    continue

                setattr(assignment, attr, value)
            
            db.session.add(assignment)
            db.session.commit()

            assignment_log = AssignmentChangeLog(
                assignment_id=assignment.id,
                detail=response["detail"]
            )
            
            db.session.add(assignment_log)
            db.session.commit()

            return make_response(assignment.to_dict(), 200)
        except Exception as error:
            print(error)
            return make_response({"message": "Error, could not update assignments"}, 404)

    def delete(self, id):
        try:
            assignment_to_delete = Assignment.query.filter_by(id=id).first()

            db.session.delete(assignment_to_delete)
            db.session.commit()

            new_asgn_log = AssignmentChangeLog(
                assignment_id=id,
                detail="Deleted Assignment"
            )

            db.session.add(new_asgn_log)
            db.session.commit()

            return make_response({}, 200)
        except:
            return make_response({"message": "Error, could not delete assignment"}, 404)
        
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
        all_log = [log.to_dict() for log in AssignmentChangeLog.query.all()]
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
