# Generated by Django 4.2.7 on 2023-12-21 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_rename_present_attendance_attendance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='studentcourse',
            name='admission_date',
            field=models.DateField(null=True),
        ),
    ]