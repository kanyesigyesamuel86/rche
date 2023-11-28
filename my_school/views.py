from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from . models import NewUser, Staffs, Students, Subjects, Year

# Create your views here.

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # You can perform additional tasks here like sending a confirmation email, logging in the user, etc.
            return redirect('login_page')  # Redirect to login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                # Handle invalid credentials
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    students = Students.objects.all()[:10] 
    teachers = Staffs.objects.all()[:10]  
    courses = Year.objects.all()[:5] 
    subjects = Subjects.objects.all()[:5]
    return render(request, 'dashboard.html', {
        'students': students,
        'teachers': teachers,
        'courses': courses,
        'subjects': subjects,
    })

@login_required
def all_users(request):
    users = NewUser.objects.all()
    return render(request, 'user_list.html', {'users':users})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_page')