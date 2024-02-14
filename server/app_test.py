from models import Employee, Project, Assignment
from app import app, db
from faker import Faker
from datetime import date, timedelta

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
                              customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China")
            
            project_2 = Project(sales_order=453498, name="KSOE Project", start_date=date(2019,2,2), expected_end_date=date(2024,2,13),
                              customer_name="KSOE", sale_price=1000000.00, comment="This is a customer from South Korea")
            
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
            pass




