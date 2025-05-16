from django.shortcuts import render

# Home Page (Dashboard)
def attendance_home(request):
    return render(request, 'attendance/attendance_home.html')


from django.shortcuts import render, redirect
from .forms import EmployeeForm

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('attendance:attendance_home')  # or any other page you want to redirect to
    else:
        form = EmployeeForm()
    return render(request, 'attendance/add_employee.html', {'form': form})


# Admin check
def is_admin(user):
    return user.is_staff


from django.shortcuts import render, redirect
from .models import Employee, Attendance
from datetime import date

def mark_attendance(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee")
        status = request.POST.get("status")

        if employee_id and status:
            employee = Employee.objects.get(id=employee_id)
            Attendance.objects.create(employee=employee, date=date.today(), status=status)
            return redirect('attendance:mark_attendance')  # Or a success page

    employees = Employee.objects.all()
    return render(request, 'attendance/mark_attendance.html',{'employees': employees})


# views.py
from django.shortcuts import render
from .models import Attendance, Employee
from datetime import date
import calendar

from django.shortcuts import render
from datetime import datetime
from .models import Attendance  # Example model


import pandas as pd
from django.http import HttpResponse
from .models import Attendance, Employee
from datetime import date
import calendar

def export_excel(request):
    year_param = request.GET.get('year')
    month_param = request.GET.get('month')

    try:
        year = int(year_param) if year_param else date.today().year
        month = int(month_param) if month_param else date.today().month
    except ValueError:
        return HttpResponse("Invalid year or month.", status=400)

    days_in_month = calendar.monthrange(year, month)[1]
    dates = [date(year, month, day) for day in range(1, days_in_month + 1)]

    employees = Employee.objects.all()
    data = []

    for employee in employees:
        row = {'Employee': employee.name}
        for d in dates:
            record = Attendance.objects.filter(employee=employee, date=d).first()
            if record:
                status = record.status.lower()
                if status == 'present':
                    row[d.strftime('%b %d')] = 'Present'
                elif status == 'half':
                    row[d.strftime('%b %d')] = 'Half'
                else:
                    row[d.strftime('%b %d')] = 'Absent'
            else:
                row[d.strftime('%b %d')] = ''
        data.append(row)

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    filename = f"Attendance_{calendar.month_name[month]}_{year}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    df.to_excel(response, index=False)

    return response


# views.py

from django.shortcuts import render, get_object_or_404
from .models import Attendance, Employee, SavedMonth
from datetime import date
from django.views.decorators.http import require_POST
from .models import Attendance, Employee, SavedMonth,AttendanceMonth


from django.shortcuts import render
from calendar import monthrange
from datetime import date, timedelta
from .models import Attendance, Employee

def attendance_list(request):
    # Get month/year from URL or default to current
    month = int(request.GET.get("month", date.today().month))
    year = int(request.GET.get("year", date.today().year))

    # Get number of days in that month
    num_days = monthrange(year, month)[1]
    date_list = [date(year, month, day) for day in range(1, num_days + 1)]

    # Prepare attendance data per employee
    attendance_data = []
    employees = Employee.objects.all()

    for emp in employees:
        daily_status = []
        present_count = 0
        half_count = 0

        for single_date in date_list:
            record = Attendance.objects.filter(employee=emp, date=single_date).first()
            if record:
                if record.status == "Present":
                    daily_status.append("P")
                    present_count += 1
                elif record.status == "Absent":
                    daily_status.append("A")
                elif record.status == "Half":
                    daily_status.append("H")
                    half_count += 0.5
            else:
                daily_status.append("")  # No record

        total_attendance = present_count + half_count
        attendance_data.append({
            "name": emp.name,
            "attendance": daily_status,
            "total": f"{total_attendance}/{num_days}"
        })

    context = {
        "month_name": date(year, month, 1).strftime("%B"),
        "year": year,
        "date_list": date_list,
        "attendance_data": attendance_data
    }

    return render(request, "attendance/attendance_list.html", context)



from collections import defaultdict
from django.http import HttpResponse
import csv

def old_records_list(request):
    records = Attendance.objects.all().order_by('-date')
    monthly_data = defaultdict(list)

    # Group records by (year, month)
    for record in records:
        key = (record.date.year, record.date.month)
        monthly_data[key].append(record)

    # Build list of months
    months = [
        {
            "year": year,
            "month": month,
            "month_name": date(year, month, 1).strftime("%B")
        }
        for (year, month) in monthly_data
    ]

    context = {
        "months": sorted(months, key=lambda x: (x['year'], x['month']), reverse=True)
    }

    return render(request, "attendance/old_records_list.html", context)


import calendar
from datetime import date
from django.http import HttpResponse
import pandas as pd
from .models import Attendance, Employee

def download_attendance_excel(request, year, month):
    year = int(year)
    month = int(month)

    # Generate all dates for the month
    days_in_month = calendar.monthrange(year, month)[1]
    dates = [date(year, month, day) for day in range(1, days_in_month + 1)]

    employees = Employee.objects.all()
    data = []

    for employee in employees:
        row = {'Employee': employee.name}
        present_count = 0
        half_count = 0

        for d in dates:
            record = Attendance.objects.filter(employee=employee, date=d).first()
            if record:
                status = record.status.lower()
                if status == 'present':
                    row[d.strftime('%b %d')] = 'Present'
                    present_count += 1
                elif status == 'half':
                    row[d.strftime('%b %d')] = 'Half'
                    half_count += 0.5
                else:
                    row[d.strftime('%b %d')] = 'Absent'
            else:
                row[d.strftime('%b %d')] = ''

        # Total attendance: Present + Half (0.5 counted)
        total_present = present_count + half_count
        row['Total Attendance'] = f"{total_present}/{days_in_month}"
        data.append(row)

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"Attendance_{calendar.month_name[month]}_{year}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    df.to_excel(response, index=False)

    return response


from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.contrib import messages

def delete_employee_view(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        emp_id = request.POST.get("employee_id")
        employee = get_object_or_404(Employee, id=emp_id)
        employee.delete()
        messages.success(request, f"Employee '{employee.name}' deleted successfully.")
        return redirect('attendance:delete_employee')  # Use your app name here

    return render(request, 'attendance/delete_employee.html', {'employees': employees})
