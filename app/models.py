from django.db import models

#abstract users, parents, students and admins
from .user import User

# Create your models here.
#all models to have entry creation date, self-id


#!! VERSION 0.1. USERS ARE MASTER MODELS. 
#!! Current hierarchy - Users > Schools > Teachers/Students/Classes > Attendance/Grades

#TODO Implement shared schools schools. parent models etc. 

#model for schools w/ name, logo, address linked only to the admin profile who created it
class School(models.Model):
    #DELETE if ADMIN / FOUNDER account is deleted
    admin = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_school', null=False)
    name = models.CharField("name", max_length=128, null=False)
    altName = models.CharField(max_length=128, blank=True, null=True) #for non-english schools
    address = models.CharField(max_length=512, blank=True, null=True)
    #logo = models.ImageField('Image', upload_to='images/', blank=True, null=True)
    #address = models.CharField(max_length=128, null=False)
    phone = models.CharField(max_length=32, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    def __str__(self):
        return f"{self.name}"

#models for teachers of the school
class Teacher(models.Model):
    school = models.ForeignKey('School', on_delete=models.SET_NULL, related_name='SchoolTeacher', null=True)
    firstName = models.CharField(max_length=64, blank=False, null=False)
    lastName = models.CharField(max_length=64, blank=False, null=False)
    altName = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    social = models.CharField(max_length=64, blank=True, null=True) #for use with other contact servicers such as LINE, MESSENGER or WHATSAPP
    code = models.CharField(max_length=64, blank=True, null=True) #if they have a school ID or other form of required identifier.
    qualification = models.CharField(max_length=64, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.firstName + ' ' + self.lastName}"

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "altName": self.altName,
            "code": self.code,
            "social": self.social,
            "phone": self.phone,
            "name": self.name,
            "qualification": self.qualification
        }

#model for linking Courses + Teachers to better abstract lookup and improve lookup speeds.
#class TeacherCourse(models.Model):
    
#model for classes w/ employee id, school id, scheduled-start time, scheduled-end time, school-year
class Course(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='facility', null=False)
    subject = models.CharField(max_length=128, null=False, blank=False) #name of class
    code = models.CharField(max_length=128, null=True, blank=True)
    level = models.PositiveIntegerField(default=1)
    year = models.CharField(max_length=12, blank=True)
    description = models.TextField(max_length=512, blank=True, null=True)
    start_time = models.TimeField(null=False, blank=True, default='0:0:0')
    end_time = models.TimeField(null=False, blank=True, default='0:0:0')
    timestamp = models.DateTimeField(auto_now_add=True)

    teacher = models.ForeignKey('User', on_delete=models.CASCADE, related_name='course', null=True, blank=True)
    #course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='teacher', null=False)
    startDate = models.DateField(auto_now_add=False, null=True, blank=True)
    endDate = models.DateField(auto_now_add=False, null=True, blank=True)


    def __str__(self):
        return f"{self.code + ' ' + self.subject}"

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "subject": self.subject,
            "level": self.level,
            "year": self.year,
            "description": self.description,
            "start_time": self.start_time,
            "send_time": self.end_time
        }

#model for students w/ school id, class id, parents id, admission date, non-admission date, grade level id, identifier, name, alt-name, alt-school id
#chid of school / parent
#parent of gradebook
class Student(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='student', null=True) #DO NOT delete student info unless specified upon data deletion
    firstName = models.CharField(max_length=64, blank=False, null=False)
    lastName = models.CharField(max_length=64, blank=False, null=False)
    altName = models.CharField(max_length=64, blank=True, null=True)
    gradeLevel = models.CharField(max_length=2, blank=False, null=False)
    identifier = models.CharField(max_length=64, blank=True, null=True)
    start_date = models.DateField(auto_now_add=False, blank=True, null=True)
    end_date = models.DateField(auto_now_add=False, blank=True, null=True)
    birthday = models.DateField(auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstName + ' ' + self.lastName}"

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "altName": self.altName,
            "gradeLevel": self.gradeLevel,
            "identifier": self.identifier,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "birthday": self.birthday,
        }

#model for linking courses and students to better abstract lookup and improve lookup speeds. 
class StudentCourse(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='admit', null=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='admission', null=False)
    admissionDate = models.DateField(auto_now_add=False, null=True, blank=True)
    status = models.BooleanField(default=True, null=False)

    def __str__(self):
        return f"{self.course, self.student}"

#model for student attendance w/ student id, date, event id
#child of student models
class Attendance(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="attending_school", null=False)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name="attendee",null=False)
    present = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=False, blank=False, null=False)
    event = models.CharField(max_length=256, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student + ' ' + self.date}"

    def serializer(self):
        return {
            "id": self.id,
            "school": self.school,
            "student": self.student,
            "present": self.present,
            "date": self.date,
            "event": self.event
        }

#model for assignment tags to sort grades and speed up grade calculation
class Assignment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="assignment")
    topic = models.CharField(max_length=64, null=False, blank=False)
    maxScore = models.IntegerField(default=0)
    minScore = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.topic}"

    def serializer(self):
        return {
            "id": self.id,
            "course": self.course,
            "topic": self.topic,
            "maxScore": self.maxScore,
            "minScore": self.minScore
        }

#model for gradebook w/ class id, student id, grade category, grade percentage, grade numerical (G,F,P, etc.), details, date
class Grade(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='grade', null=False)
    topic = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='topicGrade')
    gradeValue = models.IntegerField(default=0, null=False, blank=False) #used for percent and letter grade calculations
    weight = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    week = models.IntegerField(default=1) #used to calculate a week based performance
    notes = models.CharField(max_length=516, default='None')
    year = models.CharField(max_length=12, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student + ' ' + self.topic}"

    def serializer(self):
        return {
            "id": self.id,
            "student": self.student,
            "topic": self.topic,
            "gradeValue": self.gradeValue,
            "weight": self.weight,
            "week": self.week,
            "notes": self.notes,
            "year": self.year
        }
    
    def __str__(self):
        return f"{self.topic}"

#model for overall course grade that cumilates all grades
class CourseGrade(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='courseGrade')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='courseGrade_student')
    firstSemester = models.IntegerField(default=0)
    secondSemester = models.IntegerField(default=0)
    thirdSemester = models.IntegerField(default=0)
    fourthSemester = models.IntegerField(default=0)
    final = models.IntegerField(default=0)
    year = models.CharField(max_length=12, blank=False)

    def __str__(self):
        return f"{self.student + ' ' + self.course}"

    def serializer(self):
        return {
            "id": self.id,
            "course": self.course,
            "firstSemester": self.firstSemester,
            "secondSemester": self.secondSemester,
            "thirdSemester": self.thirdSemester,
            "fourthSemester": self.fourthSemester,
            "final": self.final,
            "year": self.year
        }


#TODO
#model for payments w/ student id, parents id, date

#model for calendar w/ school id, school-year, start date, end date

#model for events w/ calendar id, start-date, end-date, name, details, employee id or null, student id or null, alt school id or null, modifier(holiday, paid-day off, unpaid day-off, special-event), approval(default true)

#model for documents w/ school id, employee id or null, class id or null, student id or null, parents id or null