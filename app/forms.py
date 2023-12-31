from django import forms
from django.db.models import Q

from .models import User, School, Course, Student, Assignment, Grade

# course related forms
class CourseForm(forms.ModelForm):  

    class Meta():
        model = Course
        fields = ('teacher','name','subject','level','description', 'location', 'max_students', 'start_time', 'end_time', 'start_date', 'end_date')

        widgets = {
            #'grade_type': forms.Select(choices = (
            #(0, 'Point/Percent System (0%-100%)'),
            #(1, 'Letter Grade System (A-F, Complete/Incomplete, etc.)'),
            #(2, 'Point/Lettergrade Combination')),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, school, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.filter(school=school, is_teacher=True))
        self.fields['teacher'].required = False

# student related forms
class StudentForm(forms.ModelForm):  

    class Meta():
        model = Student
        fields = ('first_name','last_name','birthday','level','contact', 'start_date', 'end_date', 'admitted', 'nonadmission_type')

        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssignmentForm(forms.ModelForm):

    class Meta():
        model = Assignment
        fields = ('name', 'max_score', 'min_score', 'assigned_date', 'due_date')

        widgets = {
            'assigned_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):

    class Meta():
        model = Grade
        fields = ('grade_value', 'date')

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }