from models import Employee, Project, Assignment
from app import app, db
from faker import Faker
from datetime import date, timedelta
import ipdb
from datetime import datetime
import pytest

fake = Faker()

class TestModel:
    '''Testing models'''

    def employee_validation(self):
        '''Validates employee attributes'''
        with app.app_context():

            with pytest.raises(ValueError):
                Employee(name=None)

    def project_validation(self):
        '''Validates project attributes'''
        with app.app_context():

            with pytest.raises(ValueError):
                Project(name=None)

    def assignment_validation(self):
        '''Assignment must have allowable dates'''

        project1 = Project(sales_order=453567, name="Hanwa Project", start_date=date(2020,12,20), expected_end_date=date(2021,3,4),
                customer_name="Hanwa Ocean", sale_price=500000.00, comment="This is a customer from China", isComplete=False)
        employee1 = Employee(first_name="Travis", last_name="Browne", department="Engineering", role="Project Engineer")

        db.session.add_all([project1, employee1])
        db.session.commit()

        with pytest.raises(ValueError):
            '''Returns error if start date is before project start date'''
            Assignment(
                employee_id=employee1.id,
                project_id=project1.id,
                name="tester",
                comments="tester",
                start_date=date(2001,1,1),
                expected_end_date=date(2021,1,1)
            )

        with pytest.raises(ValueError):
            '''Return error if start date is after project end date'''
            Assignment(
                employee_id=employee1.id,
                project_id=project1.id,
                name="tester",
                comments="tester",
                start_date=date(2090,1,1),
                expected_end_date=date(2021,1,1)
            )
        
        with pytest.raises(ValueError):
            '''Returns error if end date is before project start date'''
            Assignment(
                employee_id=employee1.id,
                project_id=project1.id,
                name="tester",
                comments="tester",
                start_date=date(2021,1,1),
                expected_end_date=date(2021,3,3)
            )

        with pytest.raises(ValueError):
            '''Returns error if end date is after project end date'''
            Assignment(
                employee_id=employee1.id,
                project_id=project1.id,
                name="tester",
                comments="tester",
                start_date=date(2021,1,1),
                expected_end_date=date(2039,3,4)
            )


        