# Generated by Django 4.2.7 on 2023-12-31 16:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256)),
                ('phone', models.CharField(blank=True, max_length=32)),
                ('social', models.CharField(blank=True, max_length=64, null=True)),
                ('tag', models.CharField(blank=True, max_length=64, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_parent', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='none', max_length=64)),
                ('assigned_date', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('letter', models.CharField(default='None', max_length=12)),
                ('max_score', models.IntegerField(default=0)),
                ('min_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, null=True)),
                ('subject', models.CharField(max_length=128)),
                ('grade_type', models.PositiveIntegerField(default=0)),
                ('code', models.CharField(blank=True, max_length=128, null=True)),
                ('level', models.CharField(blank=True, max_length=24, null=True)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
                ('online', models.BooleanField(blank=True, default=False, null=True)),
                ('location', models.CharField(blank=True, max_length=128, null=True)),
                ('student_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('max_students', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('open', models.BooleanField(default=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, default='0:0:0')),
                ('end_time', models.TimeField(blank=True, default='0:0:0')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_added_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, default=0, null=True)),
                ('semester', models.IntegerField(blank=True, default=1, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=516)),
                ('grade', models.IntegerField(default=0)),
                ('grade_letter', models.CharField(default='none', max_length=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignmentGrade', to='app.assignment')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gradeCourse', to='app.course')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True)),
                ('address', models.CharField(max_length=512, null=True)),
                ('phone', models.CharField(max_length=32, null=True)),
                ('admin_code', models.CharField(default='aaaa-aaaa-aaaa', max_length=14)),
                ('teacher_code', models.CharField(default='aaaa-aaaa-aaaa', max_length=14)),
                ('parent_code', models.CharField(default='aaaa-aaaa-aaaa', max_length=14)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('admins', models.ManyToManyField(related_name='admin_school', to=settings.AUTH_USER_MODEL)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_school', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64, null=True)),
                ('last_name', models.CharField(max_length=64, null=True)),
                ('birthday', models.DateField(null=True)),
                ('level', models.CharField(max_length=2, null=True)),
                ('contact', models.CharField(max_length=64, null=True)),
                ('course_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('code', models.CharField(blank=True, max_length=64, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('admitted', models.BooleanField(blank=True, default=True, null=True)),
                ('nonadmission_type', models.CharField(blank=True, max_length=12, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_added_by', to=settings.AUTH_USER_MODEL)),
                ('courses', models.ManyToManyField(blank=True, related_name='student_Courses', to='app.course')),
                ('grades', models.ManyToManyField(related_name='grades_student', to='app.grade')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='app.school')),
            ],
        ),
        migrations.AddField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='app.student'),
        ),
        migrations.CreateModel(
            name='CourseGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.BooleanField(default=1)),
                ('year', models.IntegerField(default=0)),
                ('semester', models.IntegerField(default=1)),
                ('grade_value', models.IntegerField(default=0)),
                ('grade_letter', models.CharField(default='none', max_length=12)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseGrade', to='app.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courseGrade_student', to='app.student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facility', to='app.school'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='course_students', to='app.student'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.BooleanField(default=True)),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_added_by', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attending_school', to='app.school')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendee', to='app.student')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='app.course'),
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='app.school'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
