from django.urls import path
from . import views


app_name='attendance'

urlpatterns = [
    path('attendance/', views.attendance_home, name='attendance_home'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('export/', views.export_excel, name='export_excel'),
    # urls.py
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('add_month/', views.add_month, name='add_month'),
    path('clear_months/', views.clear_months, name='clear_months'),


]
