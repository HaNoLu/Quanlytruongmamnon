
from flask import request

from app import app, db

from app.models import *
from flask_login import current_user
import hashlib
from sqlalchemy import func
from datetime import datetime


def add_User(username, password, name, **kwagrs):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User(username=username,
                password=password,
                name=name,
                email=kwagrs.get('email'),
                )
    db.session.add(user)
    db.session.commit()

def Update_All_Classes_Max_Student(new_max_student):
    db.session.query(Classes).update({Classes.max_student:new_max_student})

def check_login(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()
    if user:
        return user


def add_child(fullname, gender, classes_id, guardian_name, guardian_phone, **kwargs):
    current_count = Child.query.filter_by(classes_id=classes_id).count()
    if current_count >= Regurations.query.first().max_student :
        return False, "Lớp đã đủ 25 trẻ"
    try:
        child = Child(fullname=fullname,
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
        print("error:", e)
        return False


def check_admin(username, password, role):
    user = User.query.filter(User.username == username.strip(),
                             User.password == str(hashlib.md5(password.encode('utf-8')).hexdigest()),
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
        'total_nu': Child.query.filter(Child.gender.__eq__("Nữ")).count(),
        'total_nam': Child.query.filter(Child.gender.__eq__("Nam")).count()
    }
def Get_Regurations():
    req=Regurations.query.first()
    return{
        'max_student':req.max_student,
        'daily_meal':req.daily_meal,
        'base_tuition':req.base_tuition,
    }
def Get_Count_Classes(class_id):
    return {
        'total_nu': Child.query.filter(Child.classes_id == class_id, Child.gender.__eq__("Nữ")).count(),
        'total_nam': Child.query.filter(Child.classes_id == class_id, Child.gender.__eq__("Nam")).count(),
        'total': Child.query.filter(Child.classes_id == class_id).count()
    }

def add_health_record(child_id, weight, temperature, note):
    try:
        record = HealthRecord(child_id=child_id,
                              weight=weight,
                              temperature=temperature,
                              note=note)
        db.session.add(record)
        db.session.commit()

        msg = "Ghi nhận sức khỏe thành công!"
        if float(temperature) > 37.5:
            msg = "Ghi nhận sức khỏe thành công! CẢNH BÁO!!! TRẺ CÓ DẤU HIỆU BỊ SỐT!"
        return True, msg
    except Exception as e:
        print(e)
        return False, str(e)


def get_health_record_today(child_id):
    today = datetime.now().date()
    return HealthRecord.query.filter(
        HealthRecord.child_id == child_id,
        func.date(HealthRecord.date) == today
    ).first()


def save_health_record(child_id, weight, temperature, note):
    try:
        record = get_health_record_today(child_id)

        if record:
            record.weight = weight
            record.temperature = temperature
            record.note = note
        else:
            record = HealthRecord(child_id=child_id,
                                  weight=weight,
                                  temperature=temperature,
                                  note=note,
                                  date=datetime.now())
            db.session.add(record)

        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi save_health: {e}")
        db.session.rollback()
        return False


def create_receipt(child_id, month, year, meal_days):
    BASIC_FEE = 1500000
    MEAL_PRICE = 25000

    total = BASIC_FEE + (int(meal_days) * MEAL_PRICE)

    try:
        receipt = Receipt(child_id=child_id,
                          month=month,
                          year=year,
                          meal_days=meal_days,
                          total_amount=total,
                          status=False)
        db.session.add(receipt)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def get_receipt(child_id, month, year):
    return Receipt.query.filter_by(child_id=child_id, month=month, year=year).first()


def save_receipt_batch(child_id, month, year, meal_days, is_paid):
    req=Regurations.query.first()
    BASIC_FEE = req.base_tuition
    MEAL_PRICE = req.daily_meal
    total = BASIC_FEE + (int(meal_days) * MEAL_PRICE)

    try:
        receipt = get_receipt(child_id, month, year)
        if receipt:
            if receipt.status == True and is_paid == True:
                pass
            elif receipt.status == True and is_paid == False:
                receipt.status = False
            else:
                receipt.meal_days = meal_days
                receipt.total_amount = total
                receipt.status = is_paid
        else:
            receipt = Receipt(child_id=child_id,
                              month=month,
                              year=year,
                              meal_days=meal_days,
                              total_amount=total,
                              status=is_paid)
            db.session.add(receipt)

        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi save_receipt: {e}")
        db.session.rollback()
        return False
def get_revenue(month, year):
    revenue = db.session.query(func.sum(Receipt.total_amount)) \
        .filter(Receipt.month == month, Receipt.year == year, Receipt.status == True) \
        .scalar()
    return revenue or 0


def get_child_by_id(child_id):
    return Child.query.get(child_id)

