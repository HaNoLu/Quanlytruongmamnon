from tkinter.font import names

from flask_admin import Admin,AdminIndexView,expose,BaseView
from flask_admin.contrib.sqla import ModelView
from app import app,db,utils
from app.models import *
from flask import redirect,url_for,request
from flask_login import current_user,login_user,logout_user
class AuthenticationModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)
class myAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')
class UserView(ModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['password']
    def is_accessible(self):
        return current_user.is_authenticated
class LogOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated
admin = Admin(app=app, name='ManageChildApp', template_mode='bootstrap4',index_view=myAdminIndexView())
admin.add_view(UserView(User,db.session))
admin.add_view(LogOutView(name='Đăng xuất'))

