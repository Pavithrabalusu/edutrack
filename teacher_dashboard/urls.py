from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register_view

app_name = 'teacher_dashboard'

urlpatterns = [
    # Authentication URLs
    path('register/', register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='teacher_dashboard:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('change-password/', views.change_password_view, name='change_password'),

    
    # Dashboard URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('upload/', views.upload_data_view, name='upload_data'),
    path('predictions/', views.predictions_view, name='predictions'),
    
    # Student Management URLs
    path('students/', views.student_list_view, name='student_list'),
    path('add-student/', views.add_student_view, name='add_student'),
    path('students/<int:pk>/', views.student_detail_view, name='student_detail'),
    path('students/<int:pk>/edit/', views.edit_student_view, name='edit_student'),
    path('delete/<int:student_id>/', views.delete_student_view, name='delete_student'),
    path('delete_all/', views.delete_all_students_view, name='delete_all_students'),
   
    
    # Reports URLs
    path('reports/', views.reports_view, name='reports'),
    path('export-reports/', views.export_reports_view, name='export_reports'),

]