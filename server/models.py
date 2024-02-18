from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

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
    
    serialize_rules = ("-assignments.employee","-assignments.project")

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
    project_change_log = db.relationship("ProjectChangeLog", back_populates="project")
    
    serialize_rules = ("-assignments.project", "-assignments.employee", "-project_change_log.project")

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
    assignment_change_log = db.relationship("AssignmentChangeLog", back_populates="assignment")

    serialize_rules = ("-employee.assignments", "-project.assignments", "-assignment_change_log.assignment")

    @validates("start_date")
    def validate_start_date(self, key, value):
        project_start_date = Project.query.filter(Project.id==self.project_id).first().start_date

        if value < project_start_date:
            print("ERRORS?")
            raise ValueError("Start date for assignment must be after project start date")
        return value
        
    @validates("expected_end_date")
    def validates_expected_end_date(self, key, value):
        project_end_date = Project.query.filter(Project.id==self.project_id).first().expected_end_date

        if value > project_end_date:
            raise ValueError("Assignment's expected end date must be less than the project's expected end date")
        return value
    
    def __repr__(self):
        return f'<Assignment {self.name} | Start Date: {self.start_date} | Expected End Date: {self.expected_end_date}>'
    

class AssignmentChangeLog(db.Model, SerializerMixin):
    __tablename__ = 'assignment_change_logs'

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    detail = db.Column(db.String)

    #try datetime. If I like it, keep it and change all dates to datetime please!
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    assignment = db.relationship("Assignment", back_populates="assignment_change_log")
    serialize_rules = ("-assignment.assignment_change_log",)
    
    def __repr__(self):
        return f'<Asgn Change Log ID: {self.id} | updated at: {self.updated_at}>'
    
class ProjectChangeLog(db.Model, SerializerMixin):
    __tablename__ = 'project_change_logs'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    detail = db.Column(db.String)

    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    project = db.relationship("Project", back_populates="project_change_log")
    serialize_rules = ("-project.project_change_log",)

    def __repr__(self):
        return f'<Projecy Change Log ID: {self.id} | updated at: {self.updated_at}>'


    
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


    

