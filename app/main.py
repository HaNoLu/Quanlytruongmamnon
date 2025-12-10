from app import app,utils,login
from app.models import *
import cloudinary.uploader
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
        avatar=request.files.get('avatar')
        avatar_path=None
        try:

            if(password.strip().__eq__(comfirm.strip())):
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path=res['secure_url']
                utils.add_User(name=name.strip(),
                               username=username.strip(),
                               password=str(password.strip()),
                               email=email,
                               avatar=avatar_path,)
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
if __name__ == '__main__':
    app.run(debug=True)
