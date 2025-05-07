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

def attendance_list(request):
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Get year and month from GET parameters if available
    year = request.GET.get('year', current_year)
    month = request.GET.get('month', current_month)

    # Convert to integers
    year = int(year)
    month = int(month)

    # Fetch attendance data filtered by year and month
    attendance_data = Attendance.objects.filter(date__year=year, date__month=month)

    # Get a list of all months for the sidebar
    months_list = [(year, m) for m in range(1, 13)]

    # Prepare month display (e.g., "January 2025")
    month_display = f"{datetime(year, month, 1).strftime('%B')} {year}"

    # Pass all the context to the template
    context = {
        'attendance_data': attendance_data,
        'months_list': months_list,
        'current_month': (year, month),
        'month_display': month_display,
    }

    return render(request, 'attendance/attendance_list.html', context)


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

        for single_date in date_list:
            record = Attendance.objects.filter(employee=emp, date=single_date).first()
            if record:
                if record.status == "Present":
                    daily_status.append("P")
                elif record.status == "Absent":
                    daily_status.append("A")
                elif record.status == "Half":
                    daily_status.append("H")
            else:
                daily_status.append("")  # No record
        attendance_data.append({
            "name": emp.name,
            "attendance": daily_status
        })

    context = {
        "month_name": date(year, month, 1).strftime("%B"),
        "year": year,
        "date_list": date_list,
        "attendance_data": attendance_data
    }

    return render(request, "attendance/attendance_list.html", context)




# Replace AttendanceMonth with SavedMonth in add_month and clear_months

@require_POST
def add_month(request):
    name = request.POST['month_name'].strip().lower()  # Convert to lowercase
    year = int(request.POST['year'])
    days = int(request.POST['days'])

    # Month mapping (already case-insensitive)
    MONTHS = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    month_number = MONTHS.get(name)
    if not month_number:
        return render(request, 'attendance/attendance_list.html', {
            'error': 'Invalid month name. Please enter a valid month.'
        })

    # Save the month details
    SavedMonth.objects.create(
        month_name=name.capitalize(),  # Capitalize the month name to store it properly
        month_number=month_number,
        year=year,
        days_in_month=days
    )
    return redirect('attendance:attendance_list')

@require_POST
def clear_months(request):
    SavedMonth.objects.all().delete()
    return redirect('attendance:attendance_list')
