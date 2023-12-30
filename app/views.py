
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .user import User
from .models import School, Course, Student, StudentCourse, Attendance, Assignment, Grade, CourseGrade
from .helpers import accessCodeGen
from .forms import CourseForm, StudentForm, CourseEnrollForm

#main site views
@csrf_exempt
def index(request):
    # Authenticated users can compse and view ideas
    if request.user.is_authenticated:
        #initalize user
        user = request.user
        #check is user is related to school
        if user.school:
            #check if user is a teacher
            if user.is_teacher:
                #load data necesary for page load and general usage
                courses = Course.objects.filter(teacher=user.id).order_by('start_time')
                return render(request, "app/index.html", {'courses': courses})
            else: 
                return render(request, "app/index.html")
        else: 
            return HttpResponseRedirect(reverse("setupSchool"))

    # Otherwise redirect to sign-in
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def settings(request):
    user = request.user
        
    if user.school:
        #load data necesary for page load and general usage
        courses = Course.objects.filter(teacher=user.id).order_by('start_time')
        
        if user == user.school.master:
            admins = user.school.admins.all()
            return render(request, "app/settings.html", {'courses': courses})
        else: 
            return render(request, "app/settings.html", {'courses': courses})
    else: 
        return HttpResponseRedirect(reverse("setupSchool"))

#school related views
@csrf_exempt
@login_required
def setupSchool(request, type=None):
    #initialized variables
    user = request.user
    #check if submition is post, then remove user from school
    if request.method == 'POST':
        #check if type is join
        if type == 'join':
            #if join type, get access code
            code = request.POST.get('code')
            #try for each code type, admin, teacher and parent, if none match, reditrect
            try:
                school = School.objects.get(admin_code=code)
                user.school = school
                user.is_admin = False
                user.is_teacher = False
                user.is_parent = True
                user.save()
                return HttpResponseRedirect(reverse("index"))
            except:
                try:
                    school = School.objects.get(teacher_code=code)
                    user.school = school
                    user.is_admin = False
                    user.is_teacher = False
                    user.is_parent = True
                    user.save()
                    return HttpResponseRedirect(reverse("index"))
                except:
                    try:
                        school = School.objects.get(parent_code=code)
                        user.school = school
                        user.is_admin = False
                        user.is_teacher = False
                        user.is_parent = True
                        user.save()
                        return HttpResponseRedirect(reverse("index"))
                    except:
                        return HttpResponseRedirect(reverse("index"))

        #check if join method is new school
        elif type == 'newschool':
            #initalize school object
            school = School()
            i = 0
            #get all form information
            try:
                name = request.POST.get('school_name')
                address = request.POST.get("school_address")
                phone = request.POST.get("school_phone")
                i = i+1
                print('succsess', i)
            except:
                return HttpResponseRedirect(reverse("index"))
            
            #generate course access code
            admin_code = accessCodeGen('school')
            teacher_code = accessCodeGen('school')
            parent_code = accessCodeGen('school')
            i = i+1
            print('succsess', i)
            print(admin_code)
            print(teacher_code)
            print(parent_code)
            # Attempt to create school
            try:
                school.name = name
                school.address = address
                school.phone = phone
                school.admin_code = admin_code
                school.teacher_code = teacher_code
                school.parent_code = parent_code
                school.master = user
                school.save()
                i = i+1
                print('succsess', i)
            except:
                return HttpResponseRedirect(reverse("index"))

            #attempt to relate school to user
            try:
                user.school = school
                user.is_admin = True
                user.is_teacher = True
                user.is_parent = False
                user.save()
                i = i+1
                print('succsess', i)
                return HttpResponseRedirect(reverse("index"))
            except:
                return HttpResponseRedirect(reverse("index"))
            
    if user.school:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "app/school/setupSchool.html")
    
@csrf_exempt
@login_required
def leaveSchool(request): 
    #initialized variables
    user = request.user
    #check if submition is post, then remove user from school
    if request.method == 'POST':
        #check if the user is linked to a school
        if user.school:
            #if yes then confirm user is NOT the master, if not, redirect.
            school = user.school

            if user == school.master:
                return HttpResponseRedirect(reverse("settings"))
            
            #check if user is admin at the school, if so, remove from admins list
            if user in school.admins.all():
                try:
                    print('adminCheck')
                    school.admins.remove(user)
                    school.save()
                except:
                    return HttpResponseRedirect(reverse("settings"))
            #check if user is techer, if so, remove links to all courses
            if user.is_teacher == True:
                try:
                    print('teacherCheck')
                    courses = Course.objects.filter(school=school, teacher=user)
                    for course in courses:
                        course.teacher = None
                        course.save()
                except:
                    return HttpResponseRedirect(reverse("settings"))
            #finally, remove user's link to school
            if user.school:
                try:
                    user.school = None
                    user.save()
                    return HttpResponseRedirect(reverse("index"))
                except:
                    return HttpResponseRedirect(reverse("settings"))
        else: 
            return HttpResponseRedirect(reverse("index"))

    elif user.school:
    
        if user.school.master == user:
            return HttpResponseRedirect(reverse("index"))
        else:
            courses = Course.objects.filter(teacher=user)
            course_count = len(courses)
            return render(request, "app/school/leaveSchool.html", {"courses": courses,
                                                                   "course_count": courses})
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def deleteSchool(request):
    #initialized variables
    user = request.user
    #check if submition is post, then remove user from school
    if request.method == 'POST':
        #check if the user is linked to a school
        if user.school:
            #confirm user typed in delete
            delete_confirm = request.POST.get('delete')
            delete_confirm = delete_confirm.upper()
            if delete_confirm != 'DELETE':
                return HttpResponseRedirect(reverse("settings"))
                
            #Confirm user is the master, if not, redirect.
            school = user.school
            if user != school.master:
                return HttpResponseRedirect(reverse("settings"))
            
            #delete school
            else:
                try:
                    school.delete()
                except:
                    return HttpResponseRedirect(reverse("settings"))
                
            #finally, remove user's link to school
            if user.school:
                try:
                    user.school = None
                    user.is_admin = False
                    user.is_teacher = False
                    user.is_parent = False
                    user.save()
                    return HttpResponseRedirect(reverse("index"))
                except:
                    return HttpResponseRedirect(reverse("settings"))
        else: 
            return HttpResponseRedirect(reverse("index"))

    if user.school:

        if user.school.master == user:
            courses = Course.objects.filter(school=user.school)
            courses_count = len(courses)
            students = Student.objects.filter(school=user.school)
            students = len(students)
            teachers = User.objects.filter(school=user.school, is_teacher=True)
            teachers = len(teachers) - 1
            parents = User.objects.filter(school=user.school, is_parent=True)
            if not parents:
                parents = 0
            else:
                parents = len(parents)
            return render(request, "app/school/deleteSchool.html", {"courses": courses,
                                                                    "courses_count":courses_count,
                                                                   "students": students,
                                                                   "teachers": teachers,
                                                                   "parents": parents})
            
        else:
            return HttpResponseRedirect(reverse("settings"))
    else:
        return HttpResponseRedirect(reverse("index"))

#student related views
@csrf_exempt
@login_required
def students(request, source='school', sortby='last_name'):
    #initialize user and other varriables
    user = request.user
    school = user.school
    all = False
    admitted = True
    # authenticate if user has a school
    if user.school and user.is_teacher or user.is_admin:
        #try to look up as school
        try:
            
            if source == 'school' and user.is_admin:
                #load data associated with school admitted students
                students = Student.objects.filter(school=school, admitted=True).order_by(sortby)
                student_count = len(students)
                courses = Course.objects.filter(teacher=user).order_by('start_time')
                admitted == True
                all = True
            elif source == 'teacher':
                #load data associated with teacher admitted students
                students = Student.objects.filter(school=school, teachers__id=user.id, admitted=True).order_by(sortby)
                student_count = len(students)
                courses = Course.objects.filter(teacher=user).order_by('start_time')
                admitted == True
            elif source == 'nonadmitted' and user.is_admin:
                #load data associated with user/teacher/parent
                students = Student.objects.filter(school=school, admitted=False).order_by(sortby)
                student_count = len(students)
                courses = Course.objects.filter(teacher=user).order_by('start_time')
                admitted = False
                all = True
        except:
            #load data associated with user/teacher/parent
            return HttpResponseRedirect(reverse("index"))
        #render
        print(admitted)
        return render(request, "app/students/students.html", {'courses':courses,
                                                              'student_count':student_count,
                                                                'students':students,
                                                                'all': all,
                                                                'admitted':admitted})
        
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def student(request, student_code):
    #initialize user
    user = request.user
    school = user.school
    #authenticate if user is related to school then pull student object
    if user.school:
        student = Student.objects.get(code=student_code, school=school)
        if student.school == user.school:
            courses = Course.objects.filter(teacher=user).order_by('start_time')
            return render(request, "app/students/student.html",{'student':student,
                                                              'courses':courses})
        return HttpResponseRedirect(reverse("courses"))
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def addStudent(request, student_code = None):
    #initialize data
    user = request.user
    school = user.school

    #if so check if user is linked to a school and has admin access
    if user.school and user.is_admin:

        #check if submition is POST
        if request.method == 'POST':
            #initalize student
            print(student_code)
            if student_code != None:
                student = Student.objects.get(code=student_code, school=school)
                form = StudentForm(request.POST, instance=student)
                # check if form data is valid
                if form.is_valid():
                    # save the form data to model
                    form.save()       

            else:
                form = StudentForm(request.POST)
                # check if form data is valid
                if form.is_valid():
                    # save the form data to model
                    student_model = form.save(commit=False)
                    student_model.school = school
                    student_model.code = accessCodeGen('course')
                    student_model.added_by = user
                    student_model.save()       
    
            return HttpResponseRedirect(reverse("students"))
                
        #if GET check if user has a related school
        else:
            
                if student_code != None:
                    #generate filled form
                    edit = True
                    student = Student.objects.get(code=student_code, school=school)
                    form = StudentForm(instance=student)
                    courses = Course.objects.filter(teacher=user).order_by('start_time')
                    return render(request, "app/students/addStudent.html", {'form': form,
                                                                        'edit': edit,
                                                                        'student': student,
                                                                        'courses':courses})
                #if no student code, generate blank form
                else:
                    #generate form with school object to limit teacher options to school related users
                    form = StudentForm()
                    courses = Course.objects.filter(teacher=user).order_by('start_time')
                    return render(request, "app/students/addStudent.html", {'form': form,
                                                                        'courses':courses})
    else:           
        #if all checks fail. Redirect.
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def removeStudent(request, student_code):
    #initalize user student and school
    user = request.user
    school = user.school
    student = Student.objects.get(code=student_code, school=school)

    #check if the user is linked to a school
    if user.school and user.is_admin:
        #check if request is post
        if request.method == 'POST':
            #confirm user typed in delete
            delete_confirm = request.POST.get('delete')
            delete_confirm = delete_confirm.upper()
            if delete_confirm != 'DELETE':
                return HttpResponseRedirect(reverse("student", student.code))
            
            #attempt to delete student
            else:
                try:
                    student.delete()
                except:
                    return HttpResponseRedirect(reverse("student", student.code))
                
                return HttpResponseRedirect(reverse("students"))
    
        else:
            grades = len(CourseGrade.objects.filter(student=student)) + len(Grade.objects.filter(student=student))
            return render(request, "app/students/removeStudent.html", {"student":student,
                                                                    "grades":grades})
            
    else:
        return HttpResponseRedirect(reverse("index"))

#course related views
@csrf_exempt
@login_required
def courses(request, source=None, sortby=None):
    #initialize user and other varriables
    user = request.user
    all = False
    courses_list = []
    courses = []
    # authenticate if user has a school
    if user.school:
        #try to look up as school
        try:
            if source == 'school' and user.is_admin:
                if sortby == None:
                    courses_list = Course.objects.filter(school=user.school).order_by('teacher', 'start_time')
                else:
                    courses_list = Course.objects.filter(school=user.school).order_by(sortby)
                courses = Course.objects.filter(teacher=user).order_by('start_time')
                course_count = len(courses_list)
                all = True
            elif source== 'teacher' and user.is_admin or user.is_teacher:
                #check sortby and load in that sort order
                if sortby == None:
                    courses = Course.objects.filter(teacher=user).order_by('start_time')
                else:
                    courses = Course.objects.filter(teacher=user).order_by(sortby)
                    #load data associated with user/teacher/parent
                courses_list = courses
                course_count = len(courses_list)
            
            else:
                return HttpResponseRedirect(reverse("index"))
        except:
            return HttpResponseRedirect(reverse("index"))
        #render
        return render(request, "app/courses/courses.html", {'courses':courses,
                                                            'courses_list':courses_list,
                                                            'course_count':course_count,
                                                            'all': all})
        
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def course(request, course_code):
    #initialize user
    user = request.user
    #authenticate if user is related to school then pull course object
    if user.school:
        course = Course.objects.get(code=course_code)
        if course.school == user.school:
            courses = Course.objects.filter(teacher=user).order_by('start_time')
            return render(request, "app/courses/course.html",{'course':course,
                                                              'courses':courses})
        return HttpResponseRedirect(reverse("courses"))
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def addCourse(request, course_code = None):
    #initialize data
    user = request.user
    school = user.school

    #if so check if user is linked to a school and has admin access
    if user.school and user.is_admin:

        #check if submition is POST
        if request.method == 'POST':
            #initalize course
            course = ()
            if course_code != None:
                course = Course.objects.get(code=course_code)
                form = CourseForm(school, request.POST, instance=course)
                # check if form data is valid
                if form.is_valid():
                    # save the form data to model
                    form.save()       

            else:
                form = CourseForm(school, request.POST)
                # check if form data is valid
                if form.is_valid():
                    # save the form data to model
                    print(form.data)
                    course_model = form.save(commit=False)
                    course_model.school = school
                    course_model.code = accessCodeGen('course')
                    course_model.added_by = user
                    course_model.save()       
    
            return HttpResponseRedirect(reverse("courses"))
                
        #if GET check if user has a related school
        else:
            
                if course_code != None:
                    #generate filled form
                    edit = True
                    course = Course.objects.get(code=course_code)
                    form = CourseForm(instance=course, school=school)
                    courses = Course.objects.filter(teacher=user).order_by('start_time')
                    return render(request, "app/courses/addCourse.html", {'form': form,
                                                                        'edit': edit,
                                                                        'course': course,
                                                                        'courses':courses})
                #if no course code, generate blank form
                else:
                    #generate form with school object to limit teacher options to school related users
                    form = CourseForm(school, initial={'school': school})
                    courses = Course.objects.filter(teacher=user).order_by('start_time')
                    return render(request, "app/courses/addCourse.html", {'form': form,
                                                                        'courses':courses})
    else:           
        #if all checks fail. Redirect.
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def removeCourse(request, course_code):
    #initalize user course and school
    user = request.user
    school = user.school
    course = Course.objects.get(code=course_code)

    #check if the user is linked to a school
    if user.school and user.is_admin:
        #check if request is post
        if request.method == 'POST':
            #confirm user typed in delete
            delete_confirm = request.POST.get('delete')
            delete_confirm = delete_confirm.upper()
            if delete_confirm != 'DELETE':
                return HttpResponseRedirect(reverse("course", course.code))
            
            #attempt to delete course
            else:
                try:
                    course.delete()
                except:
                    return HttpResponseRedirect(reverse("course", course.code))
                
                return HttpResponseRedirect(reverse("courses"))
    
        else:
            assignments = len(Assignment.objects.filter(course=course))
            grades = len(CourseGrade.objects.filter(course=course)) + len(Grade.objects.filter(course=course))
            return render(request, "app/courses/removeCourse.html", {"course":course,
                                                                    "assignments": assignments,
                                                                    "grades":grades})
            
    else:
        return HttpResponseRedirect(reverse("index"))

#course admission routes
@csrf_exempt
@login_required
def enroll(request, course_code):
    #initialize user
    user = request.user
    #check if user has permissions
    if user.is_admin and user.school:
        #initalize data required for function
        school = user.school
        course = Course.objects.get(code=course_code, school=school)
            
        #check if request is post
        if request.method == 'POST':
            print('check')
            if course_code != None:
                form = CourseEnrollForm(course, school, request.POST, instance=course)
                
                # check if form data is valid
                if form.is_valid():
                    # save the form data to model
                    form.save()
                    course.students = course.students_enrolled.count()
                    students = course.students_enrolled.all()
                    for student in students:
                        student.courses.add(course)
                        student.course_count = student.courses.count()
    
            return HttpResponseRedirect(reverse("courses"))
        
        else:
            #generate form with school object to limit teacher options to school related users
            form = CourseEnrollForm(course, school, instance=course)
            courses = Course.objects.filter(teacher=user).order_by('start_time')
            return render(request, "app/courses/enroll.html", {'form': form,
                                                                  'course': course,
                                                                    'courses':courses})
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def drop(request, course_code):
    return HttpResponseRedirect(reverse("index"))

#gradebook views
@csrf_exempt
@login_required
def gradebook(request, course):
    #initialize user
    user = request.user
    #authenticate if user is related to school then pull course object
    if user.school:
        course = Course.objects.get(code=course)
        if course.school == user.school:
            courses = Course.objects.filter(teacher=user).order_by('start_time')
            return render(request, "app/gradebook/gradebook.html",{'course':course,
                                                         'courses':courses})
        return HttpResponseRedirect(reverse("courses"))
    return HttpResponseRedirect(reverse("index"))

#API views
#all api routes are temporary csrf_exempt for the sake of functionality testing

