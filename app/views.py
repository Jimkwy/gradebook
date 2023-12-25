import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Lower

from .user import User
from .models import School, Course, Student, StudentCourse, Attendance, Assignment, Grade, CourseGrade
from .helpers import CodeGen

#site Generation Views
@csrf_exempt
def index(request):
    # Authenticated users can compse and view ideas
    if request.user.is_authenticated:
        
        
        user = request.user
        
        if user.school:
            #load data necesary for page load and general usage
            courses = Course.objects.filter(teacher=user.id)
            
            if user == user.school.master:
                admins = user.school.admins.all()
                return render(request, "app/index.html", {'user': user,
                                                    'admins': admins,
                                                    'courses': courses})
            else: 
                return render(request, "app/index.html", {'user': user,
                                                    'courses': courses})
        else: 
            return HttpResponseRedirect(reverse("setupSchool"))

    # Otherwise redirect to sign-in
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def courses(request):
    #initialize user
    user = request.user

    #authenticate if the user has a school
    if user.school:
        #load data necesary for page load and general usage with courses
        courses = Course.objects.filter(teacher=user.id)

        return render(request, "app/courses.html", {'courses':courses})
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def settings(request):
    return render(request, "app/settings.html")

@csrf_exempt
@login_required
def setupSchool(request):
    # Authenticated users can compse and view ideas
    if request.user.is_authenticated:
        if request.user.school:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "app/school/setupschool.html")
    
@csrf_exempt
@login_required
def leaveSchool(request, schoolName):
        
    #initialized variables
    user = request.user
    #initilize validator value
    valid = False

    #check if submition is post, then remove user from school
    if request.method == 'POST':
        #check if the user is linked to a school
        if user.school:
            #if yes then confirm user is NOT the master, if not, redirect.
            school = user.school

            if user == user.school.master:
                valid = False

            try: 
                print('remove')
                user.school = None
                user.save()
                school.admins.remove(user)
                school.save()
            except:
                valid = False
                
        if valid == True:
            return HttpResponseRedirect(reverse("index"))
        else: 
            return HttpResponseRedirect(reverse("index"))

    if user.school:
    
        if user.school.master == user:
            return HttpResponseRedirect(reverse("index"))
        else:
            courses = Course.objects.filter(school=user.school)
            return render(request, "app/school/leaveschool.html", {"user": user,
                                                                "courses": courses})
    else:
        return HttpResponseRedirect(reverse("index"))


#API views
#all api routes are temporary csrf_exempt for the sake of functionality testing
    
#API fuction for creating a new school
@csrf_exempt
@login_required
def newSchool(request):
    # Submiting a new school must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    #initialize school object
    school = School()
    user = request.user

    #pull json data from POST request
    data = json.loads(request.body)
    
    #check all required feilds are completed
    if data.get("name") is None and len(data.get("name")) == 0:
        return JsonResponse({"error": "Please provide a school name"}, status=400)
    if data.get("address") is None and len(data.get("address")) == 0:
        return JsonResponse({"error": "Please provide a school address"}, status=400)
    if data.get("phone") is None and len(data.get("phone")) == 0:
        return JsonResponse({"error": "Please provide a school phone number"}, status=400)
    #generate referal code for other users to join the school as a teacher/admin/parent
    school.code = CodeGen()
    if len(school.code) == 0:
        return JsonResponse({"error": "referal code could not be generated"}, status=500)
    #attempt to create new school object
    try:
        school.name = data["name"]
        school.address = data["address"]  
        school.phone = data["phone"]
        school.master = user
        school.save()

    except IntegrityError:
            return JsonResponse({"message": "Could not create school."}, status=400)
    
    #attempt to add the school to the users profile
    try: 
        school.admins.add(user)
        user.school = school
        user.save()
    except IntegrityError:
            return JsonResponse({"message": "Could not save school to user profile."}, status=400)
    
    return HttpResponseRedirect(reverse("index"))

#API function for joining a school with a referal code
@csrf_exempt
@login_required
def joinSchool(request):
    #check if request is POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    #pull POST JSON data
    data = json.loads(request.body)

    #check referal code was provided correctlly
    if data.get("school_code") is None and len(data.get("school_code")) != 14:
        return JsonResponse({"error": "Please provide a valid referal code"}, status=400)

    #attempt to join school as admin/teacher/parent
    try:
        schoolID = data["schoolID"]
        school = school.objcts.get(id = schoolID)
        school.admin.add(request.user)
        school.save()

        #save school to user as their primary school
        request.user.school = school
        request.user.save()

    except IntegrityError:
        return JsonResponse({"error": "no school found"}, status=400)
    
    return HttpResponseRedirect(reverse("index"))

#API function for creating a class in a teachers roster
@csrf_exempt
@login_required
def addCourse(request):
     # Submiting a new school must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    #initialize school object
    course = Course()

    #pull json data from POST request
    data = json.loads(request.body)
    
    #check all required feilds are completed
    if data.get("subject") is None and len(data.get("subject")) == 0:
        return JsonResponse({"error": "Please provide a course subject"}, status=400)
    if data.get("code") is None and len(data.get("code")) == 0:
        return JsonResponse({"error": "Please provide a course idetifyer code"}, status=400)
    if data.get("level") is None and len(data.get("phone")) == 0:
        return JsonResponse({"error": "Please provide a school phone number"}, status=400)
    
    #generate referal code for other users to join the school as a teacher/admin/parent
    school.code = CodeGen()
    if len(school.code) == 0:
        return JsonResponse({"error": "referal code could not be generated"}, status=500)
    
    #attempt to create new school object
    try:
        school.name = data["name"]
        school.address = data["address"]  
        school.phone = data["phone"]
        school.admin = request.user
        school.master = request.user
        school.save()

    except IntegrityError:
            return JsonResponse({"message": "Could not create school."}, status=400)
    
    return JsonResponse({"message": "New school created successfully."}, status=201)




