from itertools import count

from flask_admin import Admin,AdminIndexView,expose,BaseView
from flask_admin.contrib.sqla import ModelView
from app import app,db,utils
from app.models import *
from flask import redirect, url_for, request, render_template
from flask_login import current_user,login_user,logout_user

class AuthenticationModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)
class myAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')
class UserView(ModelView):
    # Ẩn cột password trong bảng
    column_exclude_list = ['password']
    # Ẩn password trong form thêm/sửa
    form_excluded_columns = ['password']
    def get_query(self):
        return super().get_query().filter( self.model.user_role==UserRole.USER)
    def is_accessible(self):
        return current_user.is_authenticated
class statsChildbyClasses_id(BaseView):
    @expose('/')
    def index(self):
        class_id=request.args.get('class_id')
        if class_id:
            return self.render('admin/stats_Child_by_Class.html',count=utils.Get_Count_Classes(class_id))
        return self.render('admin/stats_Child_by_Class.html')
    def is_accessible(self):
        return current_user.is_authenticated
class statsGenderView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/statsGender.html',count=utils.Get_Count_Gender())
    def is_accessible(self):
        return current_user.is_authenticated

class RegurationView(ModelView):
    can_delete = False
    can_edit = True
    can_create = False
    def on_model_change(self, form, model, is_created):
        new_max_student = model.max_student
        return utils.Update_All_Class_Max_Student(new_max_student)

class LogOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
    def is_accessible(self):
        return current_user.is_authenticated
admin = Admin(app=app, name='ManageChildApp', template_mode='bootstrap4',index_view=myAdminIndexView())
admin.add_view(UserView(User,db.session))
admin.add_view(statsGenderView(name='tỷ lệ nam nữ'))
admin.add_view(statsChildbyClasses_id(name='sĩ số theo lớp'))
admin.add_view(RegurationView(Regurations, db.session, name='Quy định'))
admin.add_view(LogOutView(name='Đăng xuất'))


