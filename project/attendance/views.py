from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee, Attendance
from .forms import AttendanceForm, EmployeeForm
import xlwt
from django.http import HttpResponse

# Admin check
def is_admin(user):
    return user.is_staff



from django.utils.timezone import now
from django.db.models import Case, When, Value, IntegerField

@login_required
def attendance_list(request):
    today = now().date()

    attendances = Attendance.objects.annotate(
        is_today=Case(
            When(date=today, then=Value(0)),  # 0 for today
            default=Value(1),                # 1 for other dates
            output_field=IntegerField()
        )
    ).order_by('is_today', '-date')  # Today first, then descending date

    return render(request, 'attendance/attendance_list.html', {
        'attendances': attendances
    })


@login_required
def download_attendance(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="attendance.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Attendance')

    # Sheet header
    row_num = 0
    columns = ['Employee Name', 'Date', 'Status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num])

    # Sheet data
    rows = Attendance.objects.all().values_list('employee__name', 'date', 'status')
    for row in rows:
        row_num += 1
        name, date, status = row
        ws.write(row_num, 0, name)
        ws.write(row_num, 1, date.strftime('%Y-%m-%d'))  # Format the date nicely
        ws.write(row_num, 2, 'Present' if status else 'Absent')

    wb.save(response)
    return response

def attendance_home(request):
    return render(request, 'attendance/attendance_home.html')


# views.py
from django.shortcuts import render, redirect
from .forms import EmployeeForm
from .models import Employee

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:attendance_home')  # Redirect back to the home page
    else:
        form = EmployeeForm()

    return render(request, 'attendance/add_employee.html', {'form': form})


# views.py
from django.shortcuts import render, redirect
from .forms import AttendanceForm
from .models import Attendance
from datetime import date

from django.contrib import messages
from datetime import date
from .models import Attendance  # Ensure your model is imported


@login_required
@user_passes_test(is_admin)
def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            today = date.today()

            # Check for existing attendance
            if Attendance.objects.filter(employee=employee, date=today).exists():
                messages.error(request, "Attendance already exists for this employee today.")
                return redirect('attendance:add_attendance')  # Redirect or re-render form with context

            # Set status as boolean
            status = form.cleaned_data['status']
            form.instance.status = True if status == '1' else False
            form.instance.date = today  # Set today's date manually

            form.save()
            messages.success(request, "Attendance recorded successfully.")
            return redirect('attendance:attendance_home')
    else:
        form = AttendanceForm()

    return render(request, 'attendance/add_attendance.html', {'form': form})
