# Generated by Django 4.2.7 on 2023-12-31 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_assignment_assigned_date_assignment_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='course',
        ),
    ]
