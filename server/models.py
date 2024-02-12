from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    #!!!!!! EMAIL AND PASSWORD FOR LOGIN FOR FUTURE !!!!!

    #email = db.Column(db.String, nullable=False)
    #password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name} | id: {self.id} | dept: {self.department} | Role: {self.role}>'

    

