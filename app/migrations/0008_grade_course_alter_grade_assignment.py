# Generated by Django 4.2.7 on 2023-12-31 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_grade_notes_alter_grade_semester_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gradeCourse', to='app.course'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignmentGrade', to='app.assignment'),
        ),
    ]
