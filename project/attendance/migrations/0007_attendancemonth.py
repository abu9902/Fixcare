# Generated by Django 5.2 on 2025-05-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_employee_date_of_joining_employee_profile_picture_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_name', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('days_in_month', models.IntegerField()),
            ],
        ),
    ]
