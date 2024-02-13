from models import Employee
from app import app, db
from faker import Faker

fake = Faker()

class TestApp:
    '''Flask application in app.py'''

    def test_gets_employees(self):
        '''retrieves campers with GET requests to /campers.'''
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




