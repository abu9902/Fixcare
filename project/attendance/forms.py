from django import forms
from .models import *

# forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Employee Name'})
        }

# forms.py
# forms.py
from django import forms
from .models import Attendance, Employee

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'status']  # Remove 'date' from the fields

    status = forms.ChoiceField(choices=[('1', '✔'), ('0', '❌')], widget=forms.RadioSelect)  # Radio buttons for attendance
