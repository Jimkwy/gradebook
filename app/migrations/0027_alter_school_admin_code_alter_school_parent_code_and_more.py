# Generated by Django 4.2.7 on 2023-12-28 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_user_is_admin_alter_user_is_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='admin_code',
            field=models.CharField(default='aaaa-aaaa-aaaa', max_length=14),
        ),
        migrations.AlterField(
            model_name='school',
            name='parent_code',
            field=models.CharField(default='aaaa-aaaa-aaaa', max_length=14),
        ),
        migrations.AlterField(
            model_name='school',
            name='teacher_code',
            field=models.CharField(default='aaaa-aaaa-aaaa', max_length=14),
        ),
    ]