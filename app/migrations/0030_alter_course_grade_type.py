# Generated by Django 4.2.7 on 2023-12-30 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_alter_course_grade_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='grade_type',
            field=models.PositiveIntegerField(default=0),
        ),
    ]