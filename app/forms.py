from django import forms
from django.db.models import Q

from .models import User, School, Course, Student, StudentCourse

# course related forms
class CourseForm(forms.ModelForm):  

    class Meta():
        model = Course
        fields = ('teacher','name','subject','level','description', 'location', 'start_time', 'end_time', 'start_date', 'end_date')

        widgets = {
            
        }

    def __init__(self, school, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.filter(school=school, is_teacher=True))
        self.fields['teacher'].required = False

class CourseEnrollForm(forms.ModelForm):  

    class Meta():
        model = Course
        fields = ('students_enrolled',)

        widgets = {
            
        }

    def __init__(self, course, school, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        self.fields['students_enrolled'] = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=Student.objects.filter(Q(school=school, admitted=True)))

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