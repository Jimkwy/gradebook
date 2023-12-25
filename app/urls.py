from django.urls import path

from . import views, auth

urlpatterns = [
    path("", views.index, name="index"),
    path("courses", views.courses, name="courses"),
    path("settings", views.settings, name="settings"),

    path("leaveSchool/<str:schoolName>/", views.leaveSchool, name="leaveSchool"),

    path("school/setupSchool", views.setupSchool, name="setupSchool"),
    #path("school-admin/deleteSchool", views.deleteSchool, name="deleteSchool"),
    
    #API routes
    path("newSchool", views.newSchool, name="newSchool"),
    path("joinSchool", views.joinSchool, name="joinSchool"),
    path("addCourse", views.addCourse, name="addCourse"),

    #authentiction Routes
    path("login", auth.login_user, name="login"),
    path("logout", auth.logout_user, name="logout"),
    path("register", auth.register, name="register"),
]
