from app import app
from models import Employee, db, Project, Assignment
from faker import Faker
from datetime import date, timedelta
import random

fake = Faker()

def create_employees():
    Employee.query.delete()

    all_employees = []
    departments = ["Purchasing", "Engineering", "Planning", "Human Resources", "Sales", "Accounting"]
    roles = {
        "Purchasing": ["Buyer"],
        "Engineering": ["Designer", "Project Engineer", "Project Manager"],
        "Planning": ["Planner"],
        "Human Resources": ["Generalist"],
        "Sales": ["Salesperson", "Applications Engineer"],
        "Accounting": ["Accountant"]
    }

    for _ in range(10):
        name = fake.name().split(" ")
        department = random.choice(departments)
        emp = Employee(
            first_name=name[0],
            last_name=name[1],
            department=department,
            role=random.choice(roles[department])
        )

        all_employees.append(emp)

    return all_employees


def create_projects():
    all_projects = []
    for _ in range(20):
        project = Project(
            sales_order=random.randint(400000,500000),
            name=fake.name(),
            start_date=fake.date_between_dates(date_start=date(2023,1,1), date_end=date(2024,1,1)),
            expected_end_date=fake.date_between_dates(date_start=date(2025,1,1), date_end=date(2029,1,1)),
            customer_name=fake.name(),
            sale_price=round(random.uniform(10000.00,1000000.00),2),
            comment=fake.paragraph(nb_sentences=1)
        )
        all_projects.append(project)

    return all_projects


def create_assignments():
    all_assignments = []
    employee_id_first = Employee.query.order_by(Employee.id).first().id
    employee_id_last = Employee.query.order_by(Employee.id.desc()).first().id

    project_id_first = Project.query.order_by(Project.id).first().id
    project_id_last = Project.query.order_by(Project.id.desc()).first().id

    for _ in range(40):
        project_id = random.randint(project_id_first, project_id_last)
        employee_id = random.randint(employee_id_first, employee_id_last)

        project = Project.query.filter(Project.id==project_id).first()

        assignment_start_date = project.start_date + timedelta(days=random.randint(1,300))
        assignment_end_date = project.expected_end_date - timedelta(days=random.randint(1,300))

        assignment = Assignment(
            employee_id=employee_id,
            project_id=project_id,
            name=fake.text(max_nb_chars=20),
            comments=fake.paragraph(nb_sentences=1),
            start_date=assignment_start_date,
            expected_end_date=assignment_end_date
        )

        all_assignments.append(assignment)
        print(assignment)


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



