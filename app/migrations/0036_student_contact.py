# Generated by Django 4.2.7 on 2023-12-30 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_rename_released_student_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='contact',
            field=models.CharField(max_length=64, null=True),
        ),
    ]