
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
@app.route('/stats',methods=['GET','POST'])
def stats():
    count=utils.Get_Count_Gender()
    return render_template('stats.html',count=count)
@app.context_processor  # dùng để toàn bộ hàm khác đề có classes
def common_response():
    return {
        'classes':utils.LoadClasses(),
    }
if __name__ == '__main__':
    app.run(debug=True)
