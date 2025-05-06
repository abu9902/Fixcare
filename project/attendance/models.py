from django.db import models

# models.py
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField()  # True = present, False = absent

    class Meta:
        unique_together = ('employee', 'date')  # 👈 This ensures one record per employee per day

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {'Present' if self.status else 'Absent'}"
