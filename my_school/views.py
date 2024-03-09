
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Course, Application
from .forms import ApplicationForm, SubjectForm, CourseForm
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, StudentForm, StudentForm2, NonStudentForm, ReportForm
from . models import Student, Enrollment, Assignment, Attendance, Announcement, LibraryBook, BorrowedBook, Fee, Feedback, Course, CustomUser, NonStudent, Subject, Report
from django .views import generic
from django.contrib import messages
from .decorators import hteacher_required, admin_required, teacher_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from PIL import Image
import io
import os
import time
from .tokens import account_activation_token



def access_denied(request):
    return render(request, 'access_denied.html')

def registration(request):
    return render(request, 'registration.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']
            user.save()
            NonStudent.objects.create(user=user)

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        username = request.POST.get('username')
        request.session['username']=username
        print(request.session['username'])
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until email confirmation
            # Convert and save the photo with the username as the filename
            if 'photo' in request.FILES:            
                user = form.save(commit=False)
                # Convert and save the photo with the username as the filename
                image = form.cleaned_data['photo']
                image_extension = 'jpg'  # Set the image extension to jpg
                image_io = io.BytesIO()
                image = Image.open(image)
                image = image.convert('RGB')  # Convert to RGB format if needed
                image.save(image_io, format='JPEG')
                
                # Save the processed image with the username as filename
                new_filename = f"{user.username}.{image_extension}"
                user.photo.save(new_filename, image_io, save=True)
            user.save()
            
            # Send email confirmation
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            
            return redirect('account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        NonStudent.objects.create(user=user)
        user.is_active = True
        user.email_confirmed = True
        user.save()
        request.session['firstname'] = user.first_name
        request.session['username'] = user.username
        return redirect('account_activation_complete')
    else:
        return HttpResponseBadRequest('Activation link is invalid!')

@login_required
def account_activation_complete(request):
    firstname = request.session.get('firstname')
    message = "Redirecting in 3 seconds..."
    time.sleep(3)  # Pause for 3 seconds
    return render(request, 'account_activation_complete.html', {'firstname': firstname, 'message': message})

def register_non_student_2(request):
    username = request.session.get('username')
    print(username)
    if not username:
        return redirect('register')

    user = NonStudent.objects.get(user__username=username)
    if request.method == 'POST':
        form = NonStudentForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = NonStudentForm(instance=user)
    return render(request, 'register1.html', {'form': form, 'username':user})



def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        username = request.POST.get('username')
        request.session['username']=username
        print(request.session['username'])
        if form.is_valid():
            user = form.save(commit=False)
            if 'photo' in request.FILES: 
                # Convert and save the photo with the username as the filename
                image = form.cleaned_data['photo']
                image_extension = 'jpg'  # Set the image extension to jpg
                image_io = io.BytesIO()
                image = Image.open(image)
                image = image.convert('RGB')  # Convert to RGB format if needed
                image.save(image_io, format='JPEG')
                
                # Save the processed image with the username as filename
                new_filename = f"{user.username}.{image_extension}"
                user.photo.save(new_filename, image_io, save=True)
                
            user.save()

            Student.objects.create(user=user)
            return redirect('register1')
    else:
        form = StudentForm()
    return render(request, 'register.html', {'form': form})

def register_student2(request):
    username = request.session.get('username')
    print(username)
    if not username:
        return redirect('register_student')

    user = Student.objects.get(user__username=username)
    if request.method == 'POST':
        form = StudentForm2(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = StudentForm2(instance=user)
    return render(request, 'register1.html', {'form': form, 'username':user})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class ReportCourseListView(generic.ListView):
    model = Course
    template_name = 'dashboard.html'

def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'dashboard.html', {'courses': courses})

def home(request):
    return render(request, 'home.html')

@login_required
@admin_required
def populate_database(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        subject_form = SubjectForm(request.POST)
        if 'add_course' in request.POST and course_form.is_valid():
            course_form.save()
        elif 'add_subject' in request.POST and subject_form.is_valid():
            subject_form.save()
        return redirect('populate')
    else:
        course_form = CourseForm()
        subject_form = SubjectForm()
    return render(request, 'admin/populate_database.html', {'course_form': course_form, 'subject_form': subject_form})

class CourseListView(generic.ListView):
    model = Course
    template_name = 'course_list.html'

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'detail.html'



def apply_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.course = course  # Assign the course to the application
            application.save()
            my_message =  'Your application has been submitted for review'
            return render(request, 'success.html', {'response_message':my_message})
    else:
        form = ApplicationForm(initial={'course': course_id})
    return render(request, 'apply.html', {'form': form, 'course': course})


def application_status(request, application_id):
    application = Application.objects.get(pk=application_id)
    return render(request, 'status.html', {'application': application})


def account_info(request):
    try:
        nonstudent, created = NonStudent.objects.get_or_create(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile does not exist.')
        return redirect('dashboard')
    
    data = [
        {'label': 'Position', 'value': nonstudent.role},
        {'label': 'Department', 'value': nonstudent.department},
        {'label': 'Qualifications', 'value': nonstudent.qualifications},
        {'label': 'Classes', 'value': nonstudent.course.name},
        {'label': 'Subjects', 'value': nonstudent.subject.name},
        {'label': 'Date of Joining', 'value': nonstudent.date_of_joining},
        {'label': 'Phone Number', 'value': nonstudent.phone_number},
        {'label': 'Address', 'value': nonstudent.address},
        {'label': 'Next of Kin', 'value': nonstudent.next_of_kin},
        {'label': "Next of Kin's Phone", 'value': nonstudent.next_of_kin_phone},
    ]
    return render(request, 'account_info.html', { 'nonstudent_data':data, 'nonstudent':nonstudent})

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        student = request.user.student
        report = Report.objects.filter(student=student)      
    except Student.DoesNotExist:
        messages.error(request, 'Not available.')
        return redirect('student_dashboard')
    
    context = {
        'student': student,
        'report' : report
    }
    return render(request, 'student/dashboard.html', context)

@login_required
@teacher_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


@login_required
def view_reports(request):
    student = request.user.student
    reports = Report.objects.filter(student=student)
    return render(request, 'students/reports.html', {'reports': reports})


def upload_reports(request, course_id):
    students = Student.objects.filter(course_id=course_id)
    forms = []

    if request.method == 'POST':
        for student in students:
            form = ReportForm(request.POST, request.FILES, prefix=str(student.id))
            if form.is_valid():
                report = form.save(commit=False)
                report.save()
                student.report = report
                student.save()
            forms.append(form)
        for i in forms:
            print(i)
    else:
        forms = [ReportForm(prefix=str(student.id)) for student in students]

    lists = zip(students, forms)

    return render(request, 'admin/upload_reports.html', {'lists':lists})
