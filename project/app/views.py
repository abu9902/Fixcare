import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def home(request):
    return render(request,'app/home.html')

from django.shortcuts import render, get_object_or_404
from .models import Sale

import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from .models import Sale
from django.db.models import Q


@login_required
def sales_list(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sales = Sale.objects.all()

    if query:
        sales = sales.filter(
            Q(name__icontains=query) |
            Q(customer_id__icontains=query) |
            Q(contact_number__icontains=query)  # ✅ corrected field name
        )

    if start_date and end_date:
        sales = sales.filter(created_at__date__range=[start_date, end_date])

    sales = sales.order_by('-created_at')  # optional: latest first
    return render(request, 'app/sales_list.html', {'sales': sales})

import openpyxl
from django.http import HttpResponse
from .models import Sale
from openpyxl.utils import get_column_letter
import datetime

def download_sales_excel(request):
    # Fetch all sales data
    sales = Sale.objects.all()

    # Create a new workbook and set the active sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sales Data'

    # Define header row, including all necessary fields from your Sale model
    headers = [
        'Customer ID', 'Name', 'Contact Number', 'Brand', 'Model', 'Issue', 'Color', 'Price', 'Location',
        'Notes', 'Assigned To', 'Service Type', 'Mode of Payment', 'Technician Name', 'Work Status', 'Customer Feedback', 'Lead Source', 'Created At'
    ]
    ws.append(headers)

    # Populate the worksheet with sales data
    for sale in sales:
        created_at = sale.created_at
        # Strip timezone info if it's timezone-aware
        if created_at.tzinfo is not None:
            created_at = created_at.replace(tzinfo=None)

        row = [
            sale.customer_id,
            sale.name,
            sale.contact_number,
            sale.brand,
            sale.model,
            sale.issue,
            sale.color,
            sale.price,
            sale.location,
            sale.notes,
            sale.assigned_to,
            sale.service_type,
            sale.mode_of_payment,
            sale.technician_name,
            sale.work_status,
            sale.customer_feedback,
            sale.lead_source,
            created_at.strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime without timezone
        ]
        ws.append(row)

    # Set response to serve the file as an Excel download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sales_data.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response

def customer_detail(request, customer_id):
    sale = get_object_or_404(Sale, customer_id=customer_id)
    return render(request, 'app/customer_detail.html', {'sale': sale})


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SaleForm

# Admin check
def is_admin(user):
    return user.is_staff

# @user_passes_test(is_admin)
@login_required
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sale data saved successfully!')
            return redirect('app:addsale')
    else:
        form = SaleForm()
    return render(request, 'app/add_sales.html', {'form': form})

