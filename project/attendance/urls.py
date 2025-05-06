from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('attendance_home/', views.attendance_home, name='attendance_home'),
    path('attendance_add/', views.add_attendance, name='add_attendance'),
    path('attendance/add_employee/', views.add_employee, name='add_employee'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('download_attendance/', views.download_attendance, name='download_attendance'),
]
