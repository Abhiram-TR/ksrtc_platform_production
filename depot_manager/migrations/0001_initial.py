# Generated by Django 5.1.6 on 2025-04-11 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bus_route', '0005_alter_schedule_end_time_alter_schedule_start_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('depot_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('capacity', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('registration_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('bus_type', models.CharField(choices=[('ordinary', 'Ordinary'), ('express', 'Express'), ('super_express', 'Super Express'), ('luxury', 'Luxury'), ('ac', 'Air Conditioned')], max_length=20)),
                ('seating_capacity', models.IntegerField()),
                ('manufacturing_year', models.IntegerField()),
                ('last_maintenance_date', models.DateField(blank=True, null=True)),
                ('next_maintenance_due', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('maintenance', 'Under Maintenance'), ('inactive', 'Inactive')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buses', to='depot_manager.depot')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('emp_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('driver', 'Driver'), ('conductor', 'Conductor'), ('mechanic', 'Mechanic'), ('manager', 'Manager'), ('admin', 'Administrative Staff'), ('other', 'Other')], max_length=20)),
                ('license_number', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.TextField()),
                ('date_of_birth', models.DateField()),
                ('date_of_joining', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('on_leave', 'On Leave'), ('suspended', 'Suspended'), ('retired', 'Retired'), ('terminated', 'Terminated')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='depot_manager.depot')),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_type', models.CharField(choices=[('routine', 'Routine Check'), ('repair', 'Repair'), ('overhaul', 'Overhaul'), ('emergency', 'Emergency Repair')], max_length=20)),
                ('description', models.TextField()),
                ('scheduled_date', models.DateField()),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_records', to='depot_manager.bus')),
                ('performed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_performed', to='depot_manager.employee')),
            ],
        ),
        migrations.CreateModel(
            name='TripAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_date', models.DateField()),
                ('role', models.CharField(choices=[('driver', 'Driver'), ('conductor', 'Conductor')], max_length=10)),
                ('slot', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening'), ('night', 'Night'), ('full_day', 'Full Day')], default='full_day', max_length=10)),
                ('assigned_time', models.TimeField(blank=True, null=True)),
                ('trip_executed', models.BooleanField(default=False)),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('assigned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments_made', to='depot_manager.employee')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_assignments', to='depot_manager.employee')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='bus_route.schedule')),
            ],
            options={
                'unique_together': {('employee', 'schedule', 'assignment_date', 'role')},
            },
        ),
        migrations.CreateModel(
            name='TripExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_start_time', models.TimeField(blank=True, null=True)),
                ('actual_end_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('cancelled', 'Cancelled'), ('delayed', 'Delayed'), ('partial', 'Partially Completed')], default='completed', max_length=10)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='depot_manager.tripassignment')),
            ],
        ),
        migrations.CreateModel(
            name='BusAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_date', models.DateField()),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='depot_manager.bus')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_assignments', to='bus_route.schedule')),
                ('assigned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bus_assignments_made', to='depot_manager.employee')),
            ],
            options={
                'unique_together': {('bus', 'schedule', 'assignment_date')},
            },
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('half_day', 'Half Day'), ('leave', 'On Leave')], default='absent', max_length=10)),
                ('check_in_time', models.TimeField(blank=True, null=True)),
                ('check_out_time', models.TimeField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='depot_manager.employee')),
            ],
            options={
                'unique_together': {('employee', 'date')},
            },
        ),
    ]
