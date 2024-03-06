from django import forms
from .models import Application, Student, Course, Subject, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username' ,'first_name', 'last_name' ,'email', 'password1', 'password2', 'user_type')


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [ 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city_or_District', 'country', 'date_of_birth', 'gender', 'document_name']
 
        widgets = {
           'document_name': forms.FileInput(attrs={'accept': 'application/pdf'}),
      }
    def __init__(self, *args, **kwargs):
     
       super().__init__(*args, **kwargs)
       self.fields['document_name'].help_text = "PDF format only. Maximum file size: 10MB."


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

class StudentForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name' , 'password1', 'password2')

class StudentForm2(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'roll_number', 'phone_number', 'address']
