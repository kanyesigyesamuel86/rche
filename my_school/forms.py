from django import forms
from .models import Application, Student, Course, Subject, CustomUser, NonStudent, Report, Event
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from cities_light.models import Country, City




class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username' ,'first_name', 'last_name' ,'email', 'password1', 'password2', 'photo', 'user_type')


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [ 'first_name', 'last_name', 'email', 'phone_number', 'address', 'country' , 'city_or_district', 'date_of_birth', 'gender', 'document_name']
 
        widgets = {
           'document_name': forms.FileInput(attrs={'accept': 'application/pdf'}),
           'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
      }
    def __init__(self, *args, **kwargs):
     
       super().__init__(*args, **kwargs)
       self.fields['document_name'].help_text = "PDF format only. Maximum file size: 10MB."

class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [ 'status']

 

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class StudentForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name' , 'password1', 'password2', 'photo')

class StudentForm2(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'phone_number', 'address', 'course', 'subject']
        
class NonStudentForm(forms.ModelForm):
    class Meta:
        model = NonStudent
        fields = ['role', 'department', 'date_of_joining', 'phone_number', 'address', 'next_of_kin', 'next_of_kin_phone', 'course', 'subject' ]
        widgets ={ 
            'date_of_joining' :forms.DateInput(attrs = {'placeholder':'mm/dd/yyyy', 'label':'Date of joining(e.g 12/28/2000)'}) 
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_file']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
