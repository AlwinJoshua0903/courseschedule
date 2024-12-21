from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.student_register, name='student_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admindashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add/', views.add_schedule, name='add'),
    path('', views.home, name='home'),
    path('edit/<int:batch_id>/', views.edit_schedule, name='edit'),
    path('delete/<int:batch_id>/', views.delete_schedule, name='delete'),



]