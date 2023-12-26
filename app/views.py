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
def courses(request, source):
    #initialize user and other varriables
    user = request.user
    all = False
    school_courses = []
    courses = []
    # authenticate if user has a school
    if user.school:

        if source:
            #try to look up as school
            try:
                school = School.objects.get(name=source)
                #authenticate admin status
                if user.is_admin == True:
                    #load all courses related to the school
                    school_courses = Course.objects.filter(school=user.school.id)
                    courses = Course.objects.filter(teacher=user)
                    course_count = len(school_courses)
                    all = True
                    
                else: 
                    #load data associated with user/teacher/parent
                    courses = Course.objects.filter(teacher=user)
                    course_count = len(courses)
                    all = False
            except:
                #load data associated with user/teacher/parent
                courses = Course.objects.filter(teacher=user)
                course_count = len(courses)
                all = False
                
        else:
            #load data associated with user/teacher/parent
            courses = Course.objects.filter(teacher=user.id)
            course_count = len(courses)
        #render

        return render(request, "app/courses.html", {'courses':courses,
                                                    'school_courses':school_courses,
                                                        'course_count': course_count,
                                                        'all': all})
        
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def settings(request):
    return render(request, "app/settings.html")

#data manipulation pages
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

@csrf_exempt
@login_required
def addCourse(request):
    #initialize data
    user = request.user
    school = user.school

    #check if submition is POST
    if request.method == 'POST':
        if user.school:
            if user.is_admin:
                teacher = request.POST["teacher"]
                name = request.POST["name"]
                subject = request.POST["subject"]
                level = request.POST["level"]
                year = request.POST["year"]
                description = request.POST["description"]
                start_time = request.POST["start_time"]
                end_time = request.POST["end_time"]
                start_date = request.POST["start_date"]
                end_date = request.POST["end_date"]

                # Attempt to create new user
                try:
                    course = Course()
                    course.school
                    course.teacher = Users.objects.get(id=teacher)
                    course.name = name
                    course.subject = subject
                    course.level = level
                    course.year = year
                    course.description = description
                    course.start_time = start_time
                    course.end_time = end_time
                    course.start_date = start_date
                    course.end_date = end_date
                    course.save()
                    
                except IntegrityError:
                    return render(request, "app/school/addCourse.html", {
                                            "message": "could not add course to course list"})
    print('check')
    #check if user has a related school
    if user.school:
        #check if user has admin access
        if user.is_admin:
            #load data necesary for page load and general usage
            try:
                teachers = User.objects.filter(school=school, is_teacher=True)
                courses = Course.objects.filter(teacher=user)
                return render(request, "app/school/addCourse.html", {'teachers':teachers,
                                                                     'courses':courses})
            except:
                return HttpResponseRedirect(reverse("index"))
    #if all checks fail. Redirect.
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
    school.code = CodeGen(1)
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




