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
    path("students/all/<str:source>", views.students, name="students"),
    path("students/all/<str:source>/sortby/<str:sortby>", views.students, name="students"),

    #course and gradebook routes
    path("courses/all/", views.courses, name="courses"),
    path("courses/all/<str:source>/", views.courses, name="courses"),
    path("courses/all/<str:source>/sort/<str:sortby>", views.courses, name="courses"),
    path("courses/moreinfo/<str:course_code>", views.course, name="course"),
    path("courses/course", views.addCourse, name="addCourse"),
    path("courses/course/<str:course_id>", views.addCourse, name="addCourse"),

    #gradebook routes
    path("gradebook/<str:course>", views.gradebook, name="gradebook"),
    
    #API routes

    #authentiction Routes
    path("login", auth.login_user, name="login"),
    path("logout", auth.logout_user, name="logout"),
    path("register", auth.register, name="register"),
]
