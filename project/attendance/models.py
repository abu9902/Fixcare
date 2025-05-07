from django.db import models
from datetime import date

# models.py

class Employee(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)

    profile_picture = models.ImageField(upload_to='employee_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=[
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Half', 'Half')
])

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

class MonthlySummary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # Format: 'May 2025'
    total_days = models.PositiveIntegerField()
    total_present = models.PositiveIntegerField()
    total_absent = models.PositiveIntegerField()
    present_dates = models.TextField()  # Store as CSV of dates
    absent_dates = models.TextField()   # Store as CSV of dates

    def __str__(self):
        return f"{self.employee.name} - {self.month}"


# models.py
class AttendanceMonth(models.Model):
    month_name = models.CharField(max_length=20)
    year = models.IntegerField()
    days_in_month = models.IntegerField()

    def __str__(self):
        return f"{self.month_name} {self.year}"


from django.db import models

class SavedMonth(models.Model):
    month_name = models.CharField(max_length=20)  # e.g., "January"
    month_number = models.IntegerField()          # e.g., 1 for Jan
    year = models.IntegerField()                  # e.g., 2025
    days_in_month = models.IntegerField()         # e.g., 31

    def __str__(self):
        return f"{self.month_name} {self.year}"
