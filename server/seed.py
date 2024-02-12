from app import app
from models import Employee, db
from faker import Faker
import random

fake = Faker()

if __name__ == "__main__":

    with app.app_context():

        print("Clearing db...")
        Employee.query.delete()

        employees = []
        departments = ["Purchasing", "Engineering", "Planning", "Human Resources", "Sales", "Accounting"]
        roles = {
            "Purchasing": ["Buyer"],
            "Engineering": ["Designer", "Project Engineer", "Project Manager"],
            "Planning": ["Planner"],
            "Human Resources": ["Generalist"],
            "Sales": ["Salesperson", "Applications Engineer"],
            "Accounting": ["Accountant"]
        }

        print("Seeding employees")
        for _ in range(10):
            name = fake.name().split(" ")
            first_name = name[0]
            last_name = name[1]
            department_ = random.choice(departments)
            role_ = random.choice(roles[department_])

            emp = Employee(
                first_name=first_name,
                last_name=last_name,
                department=department_,
                role=role_
            )

            employees.append(emp)

        db.session.add_all(employees)
        db.session.commit()

        print("Done seeding!")




