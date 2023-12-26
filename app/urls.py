from django.urls import path

from . import views, auth

urlpatterns = [
    path("", views.index, name="index"),
    path("courses/<str:source>", views.courses, name="courses"),
    path("settings", views.settings, name="settings"),

    #school related paths
    path("setupSchool", views.setupSchool, name="setupSchool"),
    path("addCourse", views.addCourse, name="addCourse"),
    path("leaveSchool/<str:schoolName>/", views.leaveSchool, name="leaveSchool"),
    #path("school-admin/deleteSchool", views.deleteSchool, name="deleteSchool"),
    
    #API routes
    path("newSchool", views.newSchool, name="newSchool"),
    path("joinSchool", views.joinSchool, name="joinSchool"),

    #authentiction Routes
    path("login", auth.login_user, name="login"),
    path("logout", auth.logout_user, name="logout"),
    path("register", auth.register, name="register"),
]
