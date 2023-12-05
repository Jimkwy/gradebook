import json
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Lower

from .user import User
from .models import School, Teacher, Course, Student, StudentCourse, Attendance, Assignment, Grade, CourseGrade

# Create your views here.
#site Generation Views
def index(request):
    # Authenticated users can compse and view ideas
    if request.user.is_authenticated:
        user = request.user

        school = School.objects.filter(id=user.school_id)

        print(school.name)

        classes = Course.objects.filter(teacher=user.id)

        return render(request, "app/index.html", {'user': user,
                                                  'school': school,
                                                  'classes': classes})

    # Otherwise redirect to sign-in
    else:
        return HttpResponseRedirect(reverse("login"))
#API views

