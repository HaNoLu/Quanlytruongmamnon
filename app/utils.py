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
              avatar=kwagrs.get('avatar'),
              )
    db.session.add(user)
    db.session.commit()
def check_login(username,password):
    password=str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user=User.query.filter(User.username==username.strip(),
                           User.password==password).first()
    if user:
        return user
def get_user_by_id(user_id):
    return User.query.get(user_id)