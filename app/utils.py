from app import app,db
from app.models import *
from flask_login import current_user
import hashlib
from sqlalchemy import func
def add_User(username ,password ,name ,**kwagrs):
    password =str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user =User(username=username,
              password=password,
              name=name,
              email=kwagrs.get('email'),
              )
    db.session.add(user)
    db.session.commit()
def check_login(username,password):
    password=str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user=User.query.filter(User.username==username.strip(),
                           User.password==password).first()
    if user:
        return user
def add_child(fullname,gender,classes_id,guardian_name,guardian_phone,**kwargs):
    current_count = Child.query.filter_by(classes_id=classes_id).count()
    if current_count >= 25:
        return False, "Lớp đã đủ 25 trẻ"
    try:
        child=Child(fullname=fullname,
                    classes_id=classes_id,
                    guardian_name=guardian_name,
                    guardian_phone=guardian_phone,
                    address=kwargs.get('address'),
                    gender=gender)
        db.session.add(child)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print("error:",e)
        return False
def check_admin(username,password,role):
    user=User.query.filter(User.username==username.strip(),
                           User.password==str(hashlib.md5(password.encode('utf-8')).hexdigest()),
                           User.user_role.__eq__(role)).first()
    if user:
        return user

def get_user_by_id(user_id):
    return User.query.get(user_id)
def LoadChild(class_id):
    return Child.query.filter(Child.classes_id.__eq__(class_id))
def LoadClasses():
    return Classes.query.all()
def LoadClass_by_id(class_id):
    return Child.query.filter(Child.classes_id.__eq__(class_id)).all()
def Get_Count_Gender():
    return {
        'total_nu':Child.query.filter(Child.gender.__eq__("Nữ")).count(),
        'total_nam':Child.query.filter(Child.gender.__eq__("Nam")).count()
    }