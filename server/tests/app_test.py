import ipdb
from models import Employee, Project, Assignment
from app import app, db
from faker import Faker
from datetime import date, timedelta
from datetime import datetime

fake = Faker()

class TestApp:
    '''Flask application in app.py'''

    def test_gets_employees(self):
        '''retrieves employees with GET requests to /employees.'''
        with app.app_context():
    
            employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")
            employee2 = Employee(first_name="Judah", last_name="Al-Jamed", department="Purchasing", role="Buyer")

            db.session.add_all([employee1, employee2])
            db.session.commit()

            response = app.test_client().get('/employees')
            assert response.status_code == 200
            assert response.content_type == 'application/json'

            response = response.json
            employees = Employee.query.all()

            assert [emp["id"] for emp in response] == [
                employee.id for employee in employees
            ]
            assert [emp["first_name"] for emp in response] == [
                employee.first_name for employee in employees
            ]
            assert [emp["last_name"] for emp in response] == [
                employee.last_name for employee in employees
            ]
            assert [emp["department"] for emp in response] == [
                employee.department for employee in employees
            ]
            assert [emp["role"] for emp in response] == [
                employee.role for employee in employees
            ]

    def test_gets_projects(self):
        '''retrieves projects with GET request to /projects.'''
        with app.app_context():

            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                              customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China", isComplete=False)
            
            project_2 = Project(sales_order=453498, name="KSOE Project", start_date=date(2019,2,2), expected_end_date=date(2024,2,13),
                              customer_name="KSOE", sale_price=1000000.00, comment="This is a customer from South Korea", isComplete=False)
            
            db.session.add_all([project_1, project_2])
            db.session.commit()

            response = app.test_client().get('/projects')
            assert response.status_code == 200
            assert response.content_type == 'application/json'

            response = response.json
            projects = Project.query.all()

            assert [prj["sales_order"] for prj in response] == [
                project.sales_order for project in projects
            ]
            assert [prj["name"] for prj in response] == [
                project.name for project in projects
            ]
            assert [prj["start_date"] for prj in response] == [
                str(project.start_date) for project in projects
            ]
            assert [prj["expected_end_date"] for prj in response] == [
                str(project.expected_end_date) for project in projects
            ]
            assert [prj["customer_name"] for prj in response] == [
                project.customer_name for project in projects
            ]
            assert [prj["sale_price"] for prj in response] == [
                project.sale_price for project in projects
            ]
            assert [prj["comment"] for prj in response] == [
                project.comment for project in projects
            ]

    def test_gets_assignments(self):
        '''retrieves assignments with GET request /assignments'''
        with app.app_context():
            employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")
            employee2 = Employee(first_name="Judah", last_name="Al-Jamed", department="Purchasing", role="Buyer")

            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2024,3,4),
                              customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            project_2 = Project(sales_order=453498, name="KSOE Project", start_date=date(2019,2,2), expected_end_date=date(2024,2,13),
                              customer_name="KSOE", sale_price=1000000.00, comment="This is a customer from South Korea")
            
            db.session.add_all([employee1, employee2, project_1, project_2])
            db.session.commit()

            assignment1 = Assignment(employee_id=employee1.id, project_id=project_1.id, name="finish redline", 
                                     comments="please finish this", start_date=date(2023,1,1), expected_end_date=date(2023,2,2), isComplete=False) 
            
            assignment2 = Assignment(employee_id=employee2.id, project_id=project_2.id, name="doodle on the paper", 
                                     comments="finish when you want to", start_date=date(2020,4,20), expected_end_date=date(2022,2,2), isComplete=False) 

            db.session.add_all([assignment1, assignment2])
            db.session.commit()

            response = app.test_client().get('/assignments')
            assert response.status_code == 200
            assert response.content_type == 'application/json'

            response = response.json

            assignments = Assignment.query.all()

            assert [asgn["employee_id"] for asgn in response] == [
                assignment.employee_id for assignment in assignments
            ]
            assert [asgn["project_id"] for asgn in response] == [
                assignment.project_id for assignment in assignments
            ]
            assert [asgn["name"] for asgn in response] == [
                assignment.name for assignment in assignments
            ]
            assert [asgn["comments"] for asgn in response] == [
                assignment.comments for assignment in assignments
            ]
            assert [asgn["start_date"] for asgn in response] == [
                str(assignment.start_date) for assignment in assignments
            ]
            assert [asgn["expected_end_date"] for asgn in response] == [
                str(assignment.expected_end_date) for assignment in assignments
            ]
            assert [asgn["isComplete"] for asgn in response] == [
                assignment.isComplete for assignment in assignments
            ]

            #Checks if employee and project objects include the correct assignments

            employee1_obj = Employee.query.filter_by(id=employee1.id).first()
            employee2_obj = Employee.query.filter_by(id=employee2.id).first()

            project1_obj = Project.query.filter_by(id=project_1.id).first()
            project2_obj = Project.query.filter_by(id=project_2.id).first()

            assert employee1_obj.assignments[0] == assignment1
            assert employee2_obj.assignments[0] == assignment2

            assert project1_obj.assignments[0] == assignment1
            assert project2_obj.assignments[0] == assignment2

    def test_get_specific_employee(self):
        '''Gets Specific employee'''
        with app.app_context():

            employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            project1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2024,3,4),
                              customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
        
            db.session.add_all([employee1, project1])
            db.session.commit()

            assignment1 = Assignment(employee_id=employee1.id, project_id=project1.id, name="finish redline", 
                                     comments="please finish this", start_date=date(2023,1,1), expected_end_date=date(2023,2,2), isComplete=False) 
        
            db.session.add(assignment1)
            db.session.commit()

            response = app.test_client().get(f'/employees/{employee1.id}')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            #checks to see the correct values are displayed as a response

            assert employee1.first_name == response["first_name"]
            assert employee1.last_name == response["last_name"]
            assert employee1.role == response["role"]
            assert employee1.department == response["department"]
            assert employee1.projects[0].to_dict(rules=("-project_change_log","-assignments")) == response["projects"][0]
            assert employee1.assignments[0].to_dict(rules=("-assignment_change_log","-employee","-project")) == response["assignments"][0]

            assignment_change_log = 'assignment_change_log'
            project_change_log = 'project_change_log'

            assert assignment_change_log not in employee1.assignments
            assert project_change_log not in employee1.assignments

    def test_get_specific_employee_fail(self):
        '''Return 400 status when failed'''
        with app.app_context():
            response = app.test_client().get('/employees/0')
            assert response.json.get('error') == "Could not find employee with id: 0"
            assert response.status_code == 404

    def test_get_specific_project(self):
        '''Returns specific project with project id'''
        with app.app_context():
            employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            project1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2024,3,4),
                              customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
        
            db.session.add_all([employee1, project1])
            db.session.commit()

            assignment1 = Assignment(employee_id=employee1.id, project_id=project1.id, name="finish redline", 
                                     comments="please finish this", start_date=date(2023,1,1), expected_end_date=date(2023,2,2), isComplete=False) 
        
            db.session.add(assignment1)
            db.session.commit()

            response = app.test_client().get(f'/projects/{project1.id}')
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            assert project1.sales_order == response["sales_order"]
            assert project1.name == response["name"]
            assert str(project1.start_date) == response["start_date"]
            assert str(project1.expected_end_date) == response["expected_end_date"]
            assert project1.customer_name == response["customer_name"]
            assert project1.sale_price == response["sale_price"]
            assert project1.comment == response["comment"]
            assert project1.isComplete == response["isComplete"]

            assert project1.assignments[0].to_dict(rules=("-assignment_change_log", "-employee", "-project")) == response["assignments"][0]
            assert project1.employees[0].to_dict(rules=("-assignments","-projects")) == response["employees"][0]


    def test_get_specific_project_fail(self):
        '''Return 400 status when failed'''
        with app.app_context():
            response = app.test_client().get('/projects/0')
            assert response.json.get('error') == "Could not find project with id: 0"
            assert response.status_code == 404


    def test_deletes_project(self):
        '''Deletes project thru HTTP call'''
        with app.app_context():

            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                                customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            employee_1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            db.session.add_all([project_1, employee_1])
            db.session.commit()

            assignment_1 = Assignment(employee_id=employee_1.id, project_id=project_1.id, name="doodle on the paper", 
                                comments="finish when you want to", start_date=date(2020,12,21), expected_end_date=date(2020,5,2), isComplete=False) 

            db.session.add(assignment_1)
            db.session.commit()

            prj_id = project_1.id
            asgn_id = assignment_1.id

            response = app.test_client().delete(
                f'/projects/{prj_id}'
            )

            deletedProject = Project.query.filter(Project.id == prj_id).one_or_none()
            deletedAssignment = Assignment.query.filter(Assignment.id == asgn_id).one_or_none()

            assert response.status_code == 200
            assert not deletedProject
            assert not deletedAssignment


    def test_deletes_project_error(self):
        '''Deleting project results in error'''
        with app.app_context():

            response = app.test_client().delete(
                f'/projects/0'
            )

            assert response.status_code == 404


    def test_deletes_assignment(self):
        '''Deletes assignment thru HTTP call'''
        with app.app_context():
            
            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                                customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            employee_1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            db.session.add_all([project_1, employee_1])
            db.session.commit()

            assignment_1 = Assignment(employee_id=employee_1.id, project_id=project_1.id, name="doodle on the paper", 
                                comments="finish when you want to", start_date=date(2020,12,21), expected_end_date=date(2020,5,2), isComplete=False) 

            db.session.add(assignment_1)
            db.session.commit()

            prj_id = project_1.id
            asgn_id = assignment_1.id

            response = app.test_client().delete(
                f'/assignments/{asgn_id}'
            )

            deletedAssignment = Assignment.query.filter(Assignment.id == asgn_id).one_or_none()
            deletedProject = Project.query.filter(Project.id == prj_id).one_or_none()

            assert response.status_code == 200
            assert not deletedAssignment
            assert deletedProject

    def test_delete_assignment_error(self):
        '''Deleting assignment results in error'''
        with app.app_context():

            response = app.test_client().delete(
                f'/assignments/0'
            )

            assert response.status_code == 404

    
    def test_post_employees(self):
        '''POSTS employees through HTTP call'''
        with app.app_context():
            first_name = "first_test"
            last_name = "last_test"
            department = "department_test"
            role = "role_test"

            response = app.test_client().post(
                '/employees',
                json={
                    'first_name': first_name,
                    'last_name': last_name,
                    'department': department,
                    'role': role
                }
            ).json

            assert response['id']
            assert response['first_name'] == first_name
            assert response['last_name'] == last_name
            assert response['department'] == department
            assert response['role'] == role

            employee = Employee.query.filter_by(id=response['id']).one_or_none()
            assert employee

    def test_post_employees_error(self):
        '''POSTing employee results in error'''
        with app.app_context():

            first_name = "first_test"
            last_name = "last_test"
            department = "department_test"

            response = app.test_client().post(
                '/employees',
                json={
                    'first_name': first_name,
                    'last_name': last_name,
                    'department': department,
                }
            )

            assert response.status_code == 404
            assert response.json['message'] == "Error, could not create new employee"


    def test_post_projects(self):
        '''POSTS project through HTTP call'''
        with app.app_context():
            sales_order = 333333
            name = "name_test"
            start_date = "2022-2-2"
            expected_end_date = "2023-3-3"
            customer_name = "customer_name_test"
            sale_price = 1000
            comment = "comment_test"
            isComplete = False

            response = app.test_client().post(
                '/projects',
                json={
                    'sales_order': sales_order,
                    'name': name,
                    'start_date': start_date,
                    'expected_end_date': expected_end_date,
                    'customer_name': customer_name,
                    'sale_price': sale_price,
                    'comment': comment,
                    'isComplete': isComplete
                }
            ).json

            assert response['id']
            assert response['sales_order'] == sales_order
            assert response['name'] == name
            assert datetime.strptime(response['start_date'], "%Y-%m-%d") == datetime.strptime(start_date, "%Y-%m-%d")
            assert datetime.strptime(response['expected_end_date'], "%Y-%m-%d") == datetime.strptime(expected_end_date, "%Y-%m-%d")
            assert response['customer_name'] == customer_name
            assert response['sale_price'] == sale_price
            assert response['comment'] == comment
            assert response['isComplete'] == isComplete

            project = Project.query.filter_by(id=response['id']).one_or_none()
            assert project

    def test_post_projects_error(self):
        '''POST project results in an error'''
        with app.app_context():

            name = "name_test"
            start_date = "2022-2-2"
            expected_end_date = "2023-3-3"
            customer_name = "customer_name_test"
            comment = "comment_test"
            isComplete = False

            response = app.test_client().post(
                '/projects',
                json={
                    'name': name,
                    'start_date': start_date,
                    'expected_end_date': expected_end_date,
                    'customer_name': customer_name,
                    'comment': comment,
                    'isComplete': isComplete
                }
            )

            assert response.status_code == 404
            assert response.json['message'] == "Error, could not create new project"

    def test_post_projects_start_end_date_validation_error(self):
        '''Start date cannot be greater than end date'''

        with app.app_context():

            response = app.test_client().post(
                '/projects',
                json = {
                    "sales_order": 40000,
                    "name": "tester",
                    "customer_name": "Bob",
                    "sale_price": 100,
                    "comment": "tester",
                    "start_date": "2020-1-1",
                    "expected_end_date": "2001-1-1"
                }
            )

            assert response.status_code == 404


    def test_post_assignments(self):
        '''POST assignment through HTTP call'''
        with app.app_context():
            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                                customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            employee_1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            db.session.add_all([project_1, employee_1])
            db.session.commit()

            project_id = project_1.id
            employee_id = employee_1.id
            name = "name_test"
            comments = "comments_test"
            start_date = "2021-1-1"
            expected_end_date = "2021-1-5"
            isComplete = False

            response = app.test_client().post(
                '/assignments',
                json={
                    "employee_id": employee_id,
                    "project_id": project_id,
                    "name": name,
                    "comments": comments,
                    "start_date": start_date,
                    "expected_end_date": expected_end_date,
                    "isCompete": isComplete
                }
            ).json

            assert response['id']
            assert response['employee_id'] == employee_id
            assert response['project_id'] == project_id
            assert response['name'] == name
            assert datetime.strptime(response['start_date'], "%Y-%m-%d") == datetime.strptime(start_date, "%Y-%m-%d")
            assert datetime.strptime(response['expected_end_date'], "%Y-%m-%d") == datetime.strptime(expected_end_date, "%Y-%m-%d")
            assert response['comments'] == comments
            assert response['isComplete'] == isComplete

            #check if change is reflected on projects and employees

            projAssignment = Project.query.filter(Project.id == project_id).one_or_none().assignments[0]
            empAssignment = Employee.query.filter(Employee.id == employee_id).one_or_none().assignments[0]

            actualAssignment = Assignment.query.filter_by(id=response['id']).one_or_none()

            assert actualAssignment == projAssignment
            assert actualAssignment == empAssignment

    def test_post_assignments_error(self):
        '''POSTing assignments result in an error'''
        with app.app_context():
            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                                customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            employee_1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            db.session.add_all([project_1, employee_1])
            db.session.commit()

            project_id = project_1.id
            employee_id = employee_1.id

            response = app.test_client().post(
                '/assignments',
                json={
                    "employee_id": employee_id,
                    "project_id": project_id,
                }
            )

            assert response.status_code == 404
            assert response.json['message'] == "Error, could not create new assignment"

    def test_post_assignments_start_end_date_validation_error(self):
        '''Start date cannot be greater than end date'''

        with app.app_context():

            project1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                    customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China", isComplete=False)
            employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            db.session.add_all([project1, employee1])
            db.session.commit()

            response = app.test_client().post(
                '/assignments',
                json = {
                    "employee_id": employee1.id,
                    "project_id": project1.id,
                    "name": "tester",
                    "comments": "tester",
                    "start_date": date(2021,2,1),
                    "expected_end_date": date(2021,1,1)
                }
            )

            assert response.status_code == 404


    def test_patch_project(self):
        '''PATCHing project'''
        with app.app_context():

            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                                customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            db.session.add(project_1)
            db.session.commit()

            response = app.test_client().patch(
                f'/projects/{project_1.id}',
                json = {
                    "sales_order": 999999,
                    "start_date": str(date(2023,3,3))
                }
            )

            assert response.status_code == 200
            response = response.json
            assert response["sales_order"] == project_1.sales_order
            assert datetime.strptime(response["start_date"], "%Y-%m-%d").date() == project_1.start_date

    def test_patch_project_error(self):
        '''PATCHing project results in an error'''
        with app.app_context():
            response = app.test_client().patch(
                '/projects/0',
                json = {
                    "name": None
                }
            )

            assert response.status_code == 404
            assert response.json["message"] == "Error, could not update project"

    def test_patch_assignment(self):
        '''PATCHing assignment'''
        with app.app_context():
            employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

            project_1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2024,3,4),
                              customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            
            db.session.add_all([employee1, project_1])
            db.session.commit()

            assignment1 = Assignment(employee_id=employee1.id, project_id=project_1.id, name="finish redline", 
                                     comments="please finish this", start_date=date(2023,1,1), expected_end_date=date(2023,2,2), isComplete=False) 

            db.session.add(assignment1)
            db.session.commit()

            name = "go home and rest"
            employee_id = 3

            response = app.test_client().patch(
                f'/assignments/{assignment1.id}',
                json = {
                    "name": name,
                    "employee_id": employee_id
                }
            )

            assert response.status_code == 200
            response = response.json
            assert response["name"] == assignment1.name
            assert response["employee_id"] == assignment1.employee_id

    def test_patch_assignment_error(self):
        '''PATCHing assignment results in an error'''
        with app.app_context():

            response = app.test_client().patch(
                '/assignments/0',
                json = {
                    "name": None
                }
            )

            assert response.status_code == 404
            assert response.json["message"] == "Error, could not update assignments"

    
























            
        




