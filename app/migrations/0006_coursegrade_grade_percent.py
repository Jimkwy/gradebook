# Generated by Django 4.2.7 on 2023-12-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_coursegrade_grade_letter'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursegrade',
            name='grade_percent',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
