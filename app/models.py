from django.db import models

#abstract users, parents, students and admins
from .user import User

# Create your models here.
#all models to have entry creation date, self-id


#!! VERSION 0.1. USERS ARE MASTER MODELS. 
#!! Current deletion hierarchy - User > Schools > Students/Courses > Attendance/Grades

#TODO Multilingual naming system.

#model for schools w/ name, logo, address linked only to the admin profile who created it
    #child of User - Creator
class School(models.Model):
    #DELETE if ADMIN / FOUNDER account is deleted

    #key fields
    master = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_school', null=False)
    admins = models.ManyToManyField('User', related_name='admin_school')
    
    #required fields
    name = models.CharField(max_length=128, blank=False, null=True)
    address = models.CharField(max_length=512, blank=False, null=True)
    phone = models.CharField(max_length=32, blank=False, null=True)

    #fields for requistration codes
    admin_code = models.CharField(max_length=14, blank=False, default='aaaa-aaaa-aaaa') #referal code
    teacher_code = models.CharField(max_length=14, blank=False, default='aaaa-aaaa-aaaa') #referal code
    parent_code = models.CharField(max_length=14, blank=False, default='aaaa-aaaa-aaaa') #referal code
    #logo = models.ImageField('Image', upload_to='images/', blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()

    #display settings in site admin backend
    def __str__(self):
        return f"{self.name}"

#model for classes w/ employee id, school id, scheduled-start time, scheduled-end time, school-year
    #child of School
    #not date, year, or semester specific if courses are perpetual or standardized
class Course(models.Model):
    #key fields
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='facility', null=False)
    teacher = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='teacher', null=True, blank=True)
    added_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='course_added_by', null=True, blank=True)
    #required fields for object to be created
    name = models.CharField(max_length=64, blank=False, null=True) #name of class
    subject = models.CharField(max_length=128, blank=False) #subject of class
    grade_type = models.BooleanField(default=0, blank=False) #used to set grading system
                                                             #grading systems: True= points/percent, False= letter (A-f, incomplete or complete, etc)
    
    
    #optional fields
    code = models.CharField(max_length=128, blank=True, null=True) #class identifer or differentiator(if any)
    level = models.CharField(max_length=24, blank=True, null=True)
    description = models.TextField(max_length=512, blank=True, null=True)
    online = models.BooleanField(default=False, blank=True, null=True) #if course is online(true) or inperson (false)
    location = models.CharField(max_length=128, blank=True, null=True) #physical location of class if any

    #keep track of student number in class
    students = models.PositiveIntegerField(blank=True, null=True, default=0)

    #scheduling dates and times for the class, editable
    start_date = models.DateField(auto_now_add=False, blank=True, null=True)
    end_date = models.DateField(auto_now_add=False, blank=True, null=True)

    start_time = models.TimeField(blank=True, default='0:0:0')
    end_time = models.TimeField(blank=True, default='0:0:0')
    
    timestamp = models.DateTimeField(auto_now_add=True)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.name}"

    #serializer for JSON
    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "subject": self.subject,
            "level": self.level,
            "year": self.year,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "start_date": self.start_date,
            "end_date": self.end_date
        }

#model for students w/ school id, class id, parents id, admission date, non-admission date, grade level id, identifier, name, alt-name, alt-school id
    #chid of school
class Student(models.Model):
    #key models
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='student') #DO NOT delete student info unless specified upon data deletion
    added_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='student_added_by', null=True, blank=True)
    
    #required Fields
    first_name = models.CharField(max_length=64, blank=False, null=True)
    last_name = models.CharField(max_length=64, blank=False, null=True)
    birthday = models.DateField(auto_now_add=False, blank=False, null=True)
    level = models.CharField(max_length=2, blank=False, null=True)

    #optional Fields
    code = models.CharField(max_length=64, blank=True, null=True)
    joined = models.DateField(auto_now_add=False, blank=True, null=True)
    released = models.DateField(auto_now_add=False, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.first_name + ' ' + self.last_name}"

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "level": self.level,
            "code": self.code,
            "joined": self.joined,
            "released": self.released,
        }

#model for linking courses and students to better abstract lookup and improve lookup speeds. 
    #child of both student and course. (both are nessesary for linking models)
class StudentCourse(models.Model):
    #key Fields
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='admit', null=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='admission', null=False)
    
    #required Fields
    admission_date = models.DateField(auto_now_add=False, blank=False, null=True)
    status = models.BooleanField(default=True, blank=False)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.course, self.student}"

#model for student attendance w/ student id, date, event id
    #child of student models
class Attendance(models.Model):
    #key Fields
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="attending_school")
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="attendee")
    added_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='attendance_added_by', null=True, blank=True)

    
    #required Fields
    attendance = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=False, blank=False)

    #optional Fields
    description = models.CharField(max_length=512, blank=True, null=True) #reason for absence

    timestamp = models.DateTimeField(auto_now_add=True)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.student + ' ' + self.date}"

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "student": self.student,
            "attendance": self.attendance,
            "date": self.date,
            "description": self.description
        }

#model for assignments
    #child of course
    #not date, year, or semester specific if assignments are reused in any capcity
    #assignments are course specific
class Assignment(models.Model):
    #reqired Fields
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="assignment")
    
    #Required fields
    name = models.CharField(max_length=64, blank=False, default='none')

    #dependant on grading system for the course - still required to set grade value
    letter = models.CharField(max_length=12, default='None', blank=False)
    max_score = models.IntegerField(default=0, blank=False)
    min_score = models.IntegerField(default=0, blank=False)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.name}"

    def serializer(self):
        return {
            "id": self.id,
            "course": self.course,
            "name": self.name,
            "letter": self.letter,
            "max_score": self.max_score,
            "min_score": self.min_score
        }

#model for grades w/ class id, student id, grade category, grade percentage, grade numerical (G,F,P, etc.), details, date
    #child of assignment and student 
class Grade(models.Model):
    #key fields
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='grade', null=False)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='assignmentGrade', null=True)
    
    #required Fields
    year = models.IntegerField(default=0, blank=False, null=True) #used for calculating final score
    semester = models.IntegerField(default=1, blank=False, null=True) #used for calculating semester final scores
    date = models.DateField(auto_now_add=False, blank=True, null=True) #used for calculating averages
    notes = models.CharField(max_length=516, default='None', blank=False)

    #dependant on grading system type
    grade_value = models.IntegerField(default=0, blank=False) #used for point/percent calcultions if point systems are used
    grade_letter = models.CharField(default='none', max_length=12, blank=False) #used for calculating letter grade values
    
    timestamp = models.DateTimeField(auto_now_add=True)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.student + ' ' + self.assignment + ' year' + self.year + ' semester' + self.semester}"

    def serializer(self):
        return {
            "id": self.id,
            "student": self.student,
            "assignment": self.assignment,
            "year": self.year,
            "semester": self.semester,
            "date": self.date,
            "notes": self.notes,
            "grade_value": self.grade_value,
            "grade_letter": self.grade_letter
        }
    
    def __str__(self):
        return f"{self.topic}"

#model for overall course grade that cumilates all grades
class CourseGrade(models.Model):
    #key fields
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='courseGrade')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='courseGrade_student')

    #required fields
    type = models.BooleanField(default=1, blank=False) #diferentiates if this is aggrigate entry for 0=year or 1=semester
    year = models.IntegerField(default=0, blank=False) #used for storing final score
    semester = models.IntegerField(default=1, blank=False) #used for storing semester final scores
    #dependant on grading system type
    grade_value = models.IntegerField(default=0, null=False, blank=False) #used for point/percent calcultions if point systems are used
    grade_letter = models.CharField(default='none', max_length=12, blank=False) #used for calculating letter grade values
    
    timestamp = models.DateTimeField(auto_now_add=True)

    #display settings in site admin backend
    def __str__(self):
        return f"{self.student + ' ' + self.course + ' year' + self.year + ' semester' + self.semester}"

    def serializer(self):
        return {
            "id": self.id,
            "course": self.course,
            "student": self.student,
            "year": self.year,
            "semester": self.semester,
            "grade_letter": self.grade_letter,
            "grade_value": self.grade_value
        }


#TODO
#model for payments w/ student id, parents id, date

#model for calendar w/ school id, school-year, start date, end date

#model for events w/ calendar id, start-date, end-date, name, details, employee id or null, student id or null, alt school id or null, modifier(holiday, paid-day off, unpaid day-off, special-event), approval(default true)

#model for documents w/ school id, employee id or null, class id or null, student id or null, parents id or null