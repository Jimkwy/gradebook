from django.urls import path

from . import views, auth

urlpatterns = [
    path("", views.index, name="index"),

    #API routes

    #authentiction Routes
    path("login", auth.login_user, name="login"),
    path("logout", auth.logout_user, name="logout"),
    path("register", auth.register, name="register"),
]
