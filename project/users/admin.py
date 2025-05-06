from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'role', 'dob', 'profile_pic')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
