from django.contrib import admin

# Register your models here.
from .user import User
from .models import School, Course, Student, StudentCourse, Attendance, Assignment, Grade, CourseGrade

admin.site.register(User)
admin.site.register(School)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(StudentCourse)
admin.site.register(Attendance)
admin.site.register(Assignment)
admin.site.register(Grade)
admin.site.register(CourseGrade)

# Register your models here.
