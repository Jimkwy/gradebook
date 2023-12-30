from django import forms

from .models import User, School, Course

# creating a form   
class CourseForm(forms.ModelForm):  

    class Meta():
        model = Course
        fields = ('teacher','name','subject','level', 'grade_type','description', 'start_time', 'end_time', 'start_date', 'end_date')

        widgets = {
            'grade_type': forms.Select(choices = (
            (0, 'Point/Percent System (0%-100%)'),
            (1, 'Letter Grade System (A-F, Complete/Incomplete, etc.)'),
            (2, 'Point/Lettergrade Combination')
        )),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, school, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'] = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.filter(school=school, is_teacher=True))
        self.fields['teacher'].required = False