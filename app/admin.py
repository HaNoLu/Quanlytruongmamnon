
from flask_admin import Admin,AdminIndexView,expose,BaseView
from flask_admin.contrib.sqla import ModelView
from app import app,db,utils
from app.models import *
from flask import redirect, url_for, request, render_template
from flask_login import current_user,login_user,logout_user

class AuthenticationModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class myAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role ==UserRole.ADMIN
    @expose('/')
    def index(self):
        return self.render('admin/index.html')
class UserView(ModelView):
    column_exclude_list = ['password']

    def get_query(self):
        return super().get_query().filter( self.model.user_role==UserRole.USER)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class statsChildbyClasses_id(BaseView):
    @expose('/')
    def index(self):
        class_id=request.args.get('class_id')
        if class_id:
            return self.render('admin/stats_Child_by_Class.html',count=utils.Get_Count_Classes(class_id))
        return self.render('admin/stats_Child_by_Class.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class statsGenderView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/statsGender.html',count=utils.Get_Count_Gender())
    def is_accessible(self):

        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class RegurationView(ModelView):
    can_create = False
    can_delete = False
    can_edit = True
    column_exclude_list = ['id']
    def on_model_change(self, form, model, is_created):
        new_max_student = model.max_student
        utils.Update_All_Classes_Max_Student(new_max_student)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class RevenueView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
    @expose('/')
    def index(self):
        month = request.args.get('month')
        year = request.args.get('year')
        return self.render('admin/revenue.html',revenue=utils.get_revenue(month,year),month=month,year=year)


class LogOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
admin = Admin(app=app, name='ManageChildApp', template_mode='bootstrap4',index_view=myAdminIndexView())
admin.add_view(UserView(User,db.session))

admin.add_view(RegurationView(Regurations, db.session, name = 'Quy định'))
admin.add_view(statsGenderView(name='Tỷ lệ nam nữ'))
admin.add_view(statsChildbyClasses_id(name='Sĩ số theo lớp'))
admin.add_view(RevenueView(name='Doanh thu'))

admin.add_view(LogOutView(name='Đăng xuất'))


