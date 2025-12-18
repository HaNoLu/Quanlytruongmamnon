
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
class statsView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
    @expose('/')
    def index(self):
        active_tab = request.args.get('tab', 'class_size')

        class_id = request.args.get('class_id')
        class_size_data = None
        if active_tab == 'class_size':
            if class_id:
                stats = utils.Get_Count_Classes(class_id)
                current_class = db.session.get(Classes, class_id)

                if current_class and stats:
                    class_size_data = {
                        'name': current_class.name,
                        'total': stats['total'],
                    }

        gender_chart_data = None
        if active_tab == 'gender_chart':
            if class_id:
                stats = utils.Get_Count_Classes(class_id)
                if stats:
                    gender_chart_data = {
                        'male': stats['total_nam'],
                        'female': stats['total_nu']
                    }

        revenue_data = 0
        month = request.args.get('month', datetime.now().month)
        year = request.args.get('year', datetime.now().year)
        if active_tab == 'revenue':
            revenue_data = utils.get_revenue(month, year)
        return self.render('admin/stats.html',
                      classes=utils.LoadClasses(),
                      class_id=class_id,
                      active_tab=active_tab,

                      class_size_data=class_size_data,
                      gender_chart_data=gender_chart_data,

                      revenue_data=revenue_data,
                      month=month,
                      year=year
                      )
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
admin.add_view(statsView(name='Thống Kê và Báo Cáo',endpoint='statsview'))
admin.add_view(LogOutView(name='Đăng xuất'))


