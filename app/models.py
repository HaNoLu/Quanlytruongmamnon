
from app import db,app
from enum import Enum as UserEnum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean,Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
class UserRole(UserEnum):
    ADMIN=1
    USER=2
class User(BaseModel,UserMixin):
    __tablename__ = 'user'
    name=Column(String(50),nullable=False)
    username=Column(String(50),nullable=False)
    email=Column(String(50),nullable=False)
    password=Column(String(50),nullable=False)
    avatar=Column(String(100),nullable=True)
    active=Column(Boolean,default=True )
    joined_date=Column(DateTime,default=datetime.now)
    user_role=Column(Enum(UserRole),default=UserRole.USER)
    classes=relationship("Classes",backref="user",lazy=True)
    def __str__(self):
        return self.name
class Child(BaseModel):
    __tablename__ = 'child'
    fullname=Column(String(50),nullable=False)
    gender=Column(String(3),nullable=False,default="Nam")
    guardian_name=Column(String(50),nullable=False)
    guardian_phone=Column(String(50),nullable=False)
    address=Column(String(50),nullable=False)
    is_active=Column(Boolean,default=True )
    classes_id=Column(Integer,ForeignKey('classes.id'),nullable=False)
    def __str__(self):
        return self.fullname
class Classes(BaseModel):
    __tablename__ = 'classes'
    name=Column(String(50),nullable=False)
    max_student=Column(Integer,default=25)
    user_id=Column(Integer,ForeignKey('user.id'),nullable=False)
    childs=relationship("Child",backref="classes",lazy=True)

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

