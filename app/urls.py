from django.urls import path

from . import views, auth

urlpatterns = [
    #general site routes
    path("", views.index, name="index"),
    path("settings", views.settings, name="settings"),

    #school related routes
    path("school/setup", views.setupSchool, name="setupSchool"),
    path("school/setup/<str:type>", views.setupSchool, name="setupSchool"),
    path("school/leaveschool/", views.leaveSchool, name="leaveSchool"),
    path("school/admin/deleteSchool", views.deleteSchool, name="deleteSchool"),
    path("school/settings", views.settings, name="settings"),

    #student related routes
    path("students/directory/", views.students, name="students"),
    path("students/directory/<str:source>", views.students, name="students"),
    path("students/directory/<str:source>/sortby/<str:sortby>", views.students, name="students"),
    path("students/student-more-info/<str:student_code>", views.student, name="student"),
    path("students/addstudent", views.addStudent, name="addStudent"),
    path("students/editstudent/<int:student_code>", views.addStudent, name="addStudent"),
    path("students/removestudent/<int:student_code>", views.removeStudent, name="removeStudent"),
    

    #course admission routes
    path("courses/enroll/<str:course_code>", views.enroll, name="enroll"),
    path("courses/drop/<str:student_code>", views.drop, name="drop"),
    path("students/student/course-list/<str:student_code", views.courses, name="courses"),

    #course and gradebook routes
    path("courses/directory/", views.courses, name="courses"),
    path("courses/directory/<str:source>/", views.courses, name="courses"),
    path("courses/all/<str:source>/sort/<str:sortby>", views.courses, name="courses"),
    path("courses/course-more-info/<str:course_code>", views.course, name="course"),
    path("courses/addcourse", views.addCourse, name="addCourse"),
    path("courses/editcourse/<str:course_code>", views.addCourse, name="addCourse"),
    path("courses/removecourse/<str:course_code>", views.removeCourse, name="removeCourse"),

    #gradebook routes
    path("gradebook/<str:course>", views.gradebook, name="gradebook"),
    
    #API routes

    #authentiction Routes
    path("login", auth.login_user, name="login"),
    path("logout", auth.logout_user, name="logout"),
    path("register", auth.register, name="register"),
]
