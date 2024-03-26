import ipdb
from app import app
from models import Employee, db, Project, Assignment
from faker import Faker
from datetime import date, timedelta
import random

fake = Faker()

def create_employees():
    Employee.query.delete()

    employee1 = Employee(
        first_name="AAA",
        last_name="BBB",
        department="LUNCH",
        role="SANDWICH!"
    )

    employee2 = Employee(
        first_name="CCC",
        last_name="DDD",
        department="DINNER",
        role="PASTA!"
    )

    all_employees = [employee1, employee2]

    return all_employees


def create_projects():

    project1 = Project(
        sales_order=111111,
        name="PROJECT AAA",
        start_date=date(1999,1,1),
        expected_end_date=date(2000,2,2),
        customer_name="CUSTOMER AAA",
        sale_price=100,
        comment="RAWR XD",
        isComplete=False
    )

    project2 = Project(
        sales_order=222222,
        name="PROJECT BBB",
        start_date=date(2010,1,1),
        expected_end_date=date(2020,2,2),
        customer_name="CUSTOMER BBB",
        sale_price=999,
        comment="SWAG",
        isComplete=False
    )

    all_projects = [project1, project2]

    return all_projects


def create_assignments():

    employee_id_first = Employee.query.order_by(Employee.id).first().id
    employee_id_last = Employee.query.order_by(Employee.id.desc()).first().id

    project_id_first = Project.query.order_by(Project.id).first().id
    project_id_last = Project.query.order_by(Project.id.desc()).first().id

    assignment1 = Assignment(
        employee_id=employee_id_first,
        project_id=project_id_first,
        name="ASSIGNMENT AAA",
        comments=":)))",
        start_date=date(1999,2,2),
        expected_end_date=date(1999,3,3),
        isComplete=False
    )

    assignment2 = Assignment(
        employee_id=employee_id_last,
        project_id=project_id_last,
        name="ASSIGNMENT BBB",
        comments=";[]",
        start_date=date(2015,1,1),
        expected_end_date=date(2017,1,1),
        isComplete=False
    )

    all_assignments = [assignment1, assignment2]
    
    return all_assignments


if __name__ == "__main__":

    with app.app_context():
        print("Clearing db...")
        Employee.query.delete()
        Project.query.delete()
        Assignment.query.delete()

        print("Seeding Employees...")
        employees = create_employees()
        db.session.add_all(employees)
        db.session.commit()

        print("Seeding Projects...")
        projects = create_projects()
        db.session.add_all(projects)
        db.session.commit()

        print("Seeding Assignments")
        assignments = create_assignments()
        db.session.add_all(assignments)
        db.session.commit()

        print("Done Seeding!")