
from app import db,app
from enum import Enum as UserEnum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean,Enum, Float
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

class HealthRecord(BaseModel):
    __tablename__ = 'health_record'
    date = Column(DateTime, default=datetime.now)
    weight = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    note = Column(String(200))
    child_id = Column(Integer, ForeignKey('child.id'), nullable=False)
    child = relationship("Child", backref="health_records", lazy=True)

class Receipt(BaseModel):
    __tablename__ = 'receipt'
    created_date = Column(DateTime, default=datetime.now)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    tuition_fee = Column(Float, default=150000)
    meal_days = Column(Integer, default=22)
    meal_fee_per_day = Column(Float, default=25000)
    total_amount = Column(Float)
    status = Column(Boolean, default=False)
    child_id = Column(Integer, ForeignKey('child.id'), nullable=False)
    child = relationship("Child", backref="receipts", lazy=True)
class Regurations(BaseModel):
    __tablename__ = 'regulations'
    max_student = Column(Integer, nullable=False,default=25)
    daily_meal = Column(Integer, nullable=False,default=25000)
    base_tuition = Column(Integer, nullable=False,default=1500000)

