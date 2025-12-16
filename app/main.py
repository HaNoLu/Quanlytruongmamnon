from datetime import datetime
from app import app,utils,login,admin
from app.models import *
from flask import render_template,request,redirect,url_for
from flask_login import login_user,logout_user
@app.route('/')
def main():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    err_msg=""
    if request.method.__eq__('POST'):
        name=request.form.get('name')
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email')
        comfirm=request.form.get('comfirm')

        try:

            if(password.strip().__eq__(comfirm.strip())):

                utils.add_User(name=name.strip(),
                               username=username.strip(),
                               password=str(password.strip()),
                               email=email,)

                return redirect(url_for('login_page'))
            else:
                err_msg="Mật khẩu không trùng khớp"
        except Exception as ex :
            err_msg="Hệ thống đang có lỗi!!!"+str(ex)
    return render_template('register.html',err_msg=err_msg)
@app.route('/login',methods=['GET','POST'])
def login_page():
    err_msg = ""
    if request.method.__eq__('POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        user=utils.check_login(username=username,password=password)

        if user :
            login_user(user=user)
            next = request.args.get('next', 'main')
            return redirect(url_for(next))
        else:
            err_msg="Password of Username is Fasle"
    return render_template('login.html',err_msg=err_msg)
@app.route('/user-logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))
@login.user_loader# tự gọi khi đăng nhập thành công
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)
@app.route('/admin_login',methods=['POST'])
def admin_login():
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            password = request.form.get('password')
            user = utils.check_admin(username=username,
                                     password=password,
                                     role=UserRole.ADMIN)
        if user:
            login_user(user=user)
            return redirect('/admin')
@app.route('/child',methods=['GET','POST'])
def child():
    classes=utils.LoadClasses()
    return render_template('managechild.html')
@app.route('/addchild',methods=['GET','POST'])
def addchild():
    if request.method == 'POST':
        fullname = request.form['fullname']
        gender = request.form.get('gender')
        classes_id = request.form['classes']
        guardian_name = request.form['guardian_name']
        guardian_phone = request.form['guardian_phone']
        address = request.form['address']
        utils.add_child(fullname, gender, classes_id, guardian_name, guardian_phone, address=address)
        return redirect('/')
    return render_template('addchild.html', classes=Classes.query.all())
@app.route('/loadchild/<int:class_id>',methods=['GET','POST'])
def loadchild(class_id):
    class_by_id = utils.LoadClass_by_id(class_id=class_id)
    return render_template('managechild.html', class_by_id=class_by_id)
@app.route('/edit-child/<int:child_id>', methods=['GET', 'POST'])
def edit_child(child_id):
    child = Child.query.get(child_id)
    if request.method == 'POST':
        child.fullname = request.form['fullname']
        child.gender = request.form['gender']
        child.guardian_name = request.form['guardian_name']
        child.guardian_phone = request.form['guardian_phone']
        child.address = request.form['address']
        db.session.commit()
        return redirect(url_for('loadchild', class_id=child.classes_id))

    return render_template('edit_child.html', child=child)
@app.route('/delete-child/<int:child_id>')
def delete_child(child_id):
    child = Child.query.get(child_id)
    if child:
        db.session.delete(child)
        db.session.commit()
    return redirect(request.referrer or url_for('loadchild'))
@app.context_processor  # dùng để toàn bộ hàm khác đề có classes
def common_response():
    return {
        'classes':utils.LoadClasses(),
    }

@app.route('/health', methods=['GET', 'POST'])
def health():
    class_id = request.args.get('class_id')
    children = []
    health_data = {}
    if class_id:
        children = utils.LoadChild(class_id)
        for child in children:
            record = utils.get_health_record_today(child.id)
            if record:
                health_data[child.id] = record
    
    return render_template('health.html',
                           children=children,
                           classes=utils.LoadClasses(),
                           class_id=class_id,
                           health_data=health_data)

@app.route('/add-health/<int:child_id>', methods=['POST'])
def add_health(child_id):
    weight = request.form.get('weight')
    temp = request.form.get('temperature')
    note = request.form.get('note')
    success, msg = utils.add_health_record(child_id, weight, temp, note)
    return redirect(request.referrer)

@app.route('/save-batch-health', methods=['POST'])
def save_batch_health():
    class_id = request.form.get('class_id_hidden')

    try:
        for key in request.form:
            if key.startswith('weight_'):
                id_parts = key.split('_')
                if len(id_parts) == 2:
                    child_id = id_parts[1]

                    weight = request.form.get(f'weight_{child_id}')
                    temp = request.form.get(f'temp_{child_id}')
                    note = request.form.get(f'note_{child_id}')

                    if weight and temp:
                        utils.add_health_record(child_id, weight, temp, note)
                        
        return redirect(url_for('health', class_id=class_id))
    except Exception as e:
        return f"Lỗi: {str(e)}"

@app.route('/tuition', methods=['GET', 'POST'])
def tuition():
    class_id = request.args.get('class_id')
    month = request.args.get('month', datetime.now().month)
    year = request.args.get('year', datetime.now().year)
    req=utils.Get_Regurations()
    children = []
    receipt_data = {}
    if class_id:
        children = utils.LoadChild(class_id)
        for child in children:
            receipt = utils.get_receipt(child.id, month, year)
            if receipt:
                receipt_data[child.id] = receipt

    return render_template('tuition.html',
                           children=children,
                           classes=utils.LoadClasses(),
                           class_id=class_id,
                           selected_month=int(month),
                           selected_year=int(year),
                           receipt_data=receipt_data,
                           base_tuition=req['base_tuition'],
                           mealPrice=req['daily_meal'])

@app.route('/pay-tuition/<int:child_id>', methods=['POST'])
def pay_tuition(child_id):
    month = request.form.get('month')
    year = request.form.get('year')
    meal_days = request.form.get('meal_days')
    
    if utils.create_receipt(child_id, month, year, meal_days):
        return redirect(request.referrer)
    else:
        return "Có lỗi xảy ra", 500
    
@app.route('/save-batch-tuition', methods=['POST'])
def save_batch_tuition():
    class_id = request.form.get('class_id_hidden')
    month = request.form.get('month_hidden')
    year = request.form.get('year_hidden')
    try:
        for key in request.form:
            if key.startswith('meal_days_'):
                child_id = key.split('_')[2]
                meal_days = request.form.get(f'meal_days_{child_id}')
                is_paid_raw = request.form.get(f'paid_{child_id}')
                is_paid = True if is_paid_raw else False
                utils.save_receipt_batch(child_id, month, year, meal_days, is_paid)
                
        return redirect(url_for('tuition', class_id=class_id, month=month, year=year))
    except Exception as e:
        return f"Lỗi: {str(e)}"
    
@app.route('/print-receipt/<int:child_id>', methods=['GET'])
def print_receipt(child_id):
    month = request.args.get('month')
    year = request.args.get('year')

    child = utils.get_child_by_id(child_id)
    receipt = utils.get_receipt(child_id, month, year)
    if not receipt or not child:
        return "Không tìm thấy hóa đơn hoặc dữ liệu trẻ!", 404
    basic_fee = utils.Get_Regurations['base_tuition']
    meal_price = utils.Get_Regurations['daily_meal']
    meal_total = receipt.meal_days * meal_price
    
    return render_template('receipt.html', 
                           child=child, 
                           receipt=receipt,
                           basic_fee=basic_fee,
                           meal_price=meal_price,
                           meal_total=meal_total,
                           now=datetime.now())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
