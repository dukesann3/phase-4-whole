from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    assignments = db.relationship("Assignment", back_populates="employee", cascade='all, delete-orphan')
    projects = association_proxy("assignments", "project", 
                                 creator=lambda project_obj: Assignment(project=project_obj))

    #!!!!!! EMAIL AND PASSWORD FOR LOGIN FOR FUTURE !!!!!

    #email = db.Column(db.String, nullable=False)
    #password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name} | id: {self.id} | dept: {self.department} | Role: {self.role}>'
    

class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    sales_order=db.Column(db.Integer, nullable=False)
    name=db.Column(db.String, nullable=False)
    start_date=db.Column(db.Date, nullable=False)
    expected_end_date=db.Column(db.Date, nullable=False)
    customer_name=db.Column(db.String)
    sale_price=db.Column(db.Float)
    comment=db.Column(db.String)

    assignments = db.relationship("Assignment", back_populates="project", cascade="all, delete-orphan")
    employees = association_proxy("assignments", "employee", 
                                  creator=lambda employee_obj: Assignment(employee=employee_obj))

    def __repr__(self):
        return f'<Project {self.name} | SO: {self.sales_order}>'
    

class Assignment(db.Model, SerializerMixin):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    name = db.Column(db.String, nullable=False)
    comments = db.Column(db.String)
    start_date = db.Column(db.Date, nullable=False)
    expected_end_date = db.Column(db.Date, nullable=False)

    employee = db.relationship("Employee", back_populates="assignments")
    project = db.relationship("Project", back_populates="assignments")

    def __repr__(self):
        return f'<Assignment {self.name}>'
    










# class EmployeeBoss(db.Model, SerializerMixin):
#     __tablename__ = 'employees_bosses'

#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), unique=True)
#     boss_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

#     employee = db.relationship("Employee", secondary="EmployeeBoss", back_populates="employee")

    # @validates('boss_id', 'employee_id')
    # def validates_boss_id(self, key, value):
    #     emp_boss_all = [empboss.to_dict() for empboss in EmployeeBoss.query.all()]

    #     if self.boss_id == self.employee_id:
    #         raise ValueError("Employee and Boss cannot be the same person")
        
    #     for emp_boss in emp_boss_all:
    #         employee_id = emp_boss.employee_id
    #         boss_id = emp_boss.boss_id

    #         if employee_id == self.boss_id and boss_id == self.employee_id:
    #             raise ValueError("An employee's boss cannot be an employee of his/her employees")
        

        
    # def __repr__(self):
    #     return f'<Employee_Boss_Relationship | Employee ID: {self.employee_id} | Boss ID: {self.boss_id}>'


    

