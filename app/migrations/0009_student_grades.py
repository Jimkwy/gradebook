# Generated by Django 4.2.7 on 2023-12-31 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_grade_course_alter_grade_assignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='grades',
            field=models.ManyToManyField(related_name='grades_student', to='app.grade'),
        ),
    ]
