from django.db import models
from django.utils import timezone

class Sale(models.Model):
    LEAD_SOURCES = [('Fixcare', 'Fixcare'), ('Other', 'Other')]
    SERVICE_TYPES = [
        ('Onsite', 'Onsite'),
        ('Pickup/Drop', 'Pickup/Drop'),
        ('Walkin', 'Walkin'),
        ('Rework', 'Rework'),
    ]
    PAYMENT_MODES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('None', 'None'),
    ]
    WORK_STATUSES = [
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Pending', 'Pending'),
    ]
    FEEDBACK_OPTIONS = [
        ('Good', 'Good'),
        ('Bad', 'Bad'),
        ('Neutral', 'Neutral'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)

    lead_source = models.CharField(max_length=50, choices=LEAD_SOURCES)
    customer_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    issue = models.TextField()
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    assigned_to = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)

    # New Fields
    mode_of_payment = models.CharField(max_length=10, choices=PAYMENT_MODES, default='None')
    technician_name = models.CharField(max_length=100, blank=True)
    work_status = models.CharField(max_length=20, choices=WORK_STATUSES, default='Pending')
    customer_feedback = models.CharField(max_length=10, choices=FEEDBACK_OPTIONS, default='Neutral')

    def __str__(self):
        return f"{self.name} ({self.customer_id})"
