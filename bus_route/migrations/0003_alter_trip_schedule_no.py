# Generated by Django 5.1.6 on 2025-03-08 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_route', '0002_alter_schedule_unique_together_route_order_sequence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='schedule_no',
            field=models.CharField(max_length=20),
        ),
    ]
