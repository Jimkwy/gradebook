from django.urls import path

from . import views, auth

urlpatterns = [
    path("home", views.index, name="home"),

    path("setupSchool", views.setupSchool, name="setupSchool"),
    path("leaveSchool", views.leaveSchool, name="leaveSchool"),

    #API routes
    path("newSchool", views.newSchool, name="newSchool"),
    path("joinSchool", views.joinSchool, name="joinSchool"),
    path("addCourse", views.addCourse, name="addCourse"),

    #path("leaveSchool", views.leaveSchool, name="leaveSchool"),

    #authentiction Routes
    path("login", auth.login_user, name="login"),
    path("logout", auth.logout_user, name="logout"),
    path("register", auth.register, name="register"),
]
