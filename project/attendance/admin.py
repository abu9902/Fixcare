from django.contrib import admin

# Register your models here.

from . models import *

admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(AttendanceMonth)
admin.site.register(SavedMonth)