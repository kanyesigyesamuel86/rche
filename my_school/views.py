import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, StudentForm, StudentForm2, NonStudentForm, ReportForm, ApplicationReviewForm, Application, SubjectForm, CourseForm, ApplicationForm
from . models import Student, Enrollment, Assignment, Attendance, Announcement, LibraryBook, BorrowedBook, Fee, Feedback, Course, CustomUser, NonStudent, Subject, Report, Application
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
import random
import matplotlib.pyplot as plt
from io import BytesIO
import base64



def access_denied(request):
    return render(request, 'access_denied.html')

def registration(request):
    return render(request, 'registration.html')


@login_required
@admin_required
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

@login_required
@admin_required
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        username = request.POST.get('username')
        request.session['username']=username
        print(request.session['username'])
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
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

@login_required
@admin_required
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


@login_required
@admin_required
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

@login_required
@admin_required
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

@login_required
@admin_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
@admin_required
def reports(request):
    courses = Course.objects.all()
    return render(request, 'admin/reports.html', {'courses': courses})


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
            application.status = 'review'
            application.save()
            
            my_message =  'Your application has been submitted for review'
            return render(request, 'success.html', {'response_message':my_message})
    else:
        form = ApplicationForm(initial={'course': course_id})
    return render(request, 'apply.html', {'form': form, 'course': course})


def application_status(request, application_id):
    application = Application.objects.get(pk=application_id)
    return render(request, 'status.html', {'application': application})

@login_required
def account_info(request):
    data = []

    if request.user.user_type == 'other':
        try:
            student, created = Student.objects.get_or_create(user=request.user)
        except Student.DoesNotExist:
            messages.error(request, 'Student profile does not exist.')
            return redirect('dashboard')
        
        data = [
            {'label': 'Student Number', 'value': student.user.username},
            {'label': 'Roll Number', 'value': student.roll_number},
            {'label': 'Class', 'value': student.course},
            {'label': 'Classe', 'value': student.subject.name},
            {'label': 'Subjects', 'value': student.subject.name},
            {'label': 'Phone Number', 'value': student.phone_number},
            {'label': 'Address', 'value': student.address},
      
        ]
    else:


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
    return render(request, 'account_info.html', { 'nonstudent_data':data})

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        student = request.user.student
        report = Report.objects.filter(student=student)      
    except Student.DoesNotExist:
        messages.error(request, 'Not available.')
        return redirect('home')
    
    context = {
        'student': student,
        'report' : report
    }
    return render(request, 'student/dashboard.html', context)

@login_required
@teacher_required
def teacher_dashboard(request):
    count_classes = 0
    count_subjects = 0
    count_students = 0

    class_names = []
    average_scores = []

    teacher = NonStudent.objects.get(user=request.user)
    for course in teacher.course.all():
        count_classes += 1
        class_names.append(course.name)
        average_scores.append(random.randint(50,100))
        students = Student.objects.filter(course= course)
        count_students+= len(students)
    print('graphs:', class_names, average_scores)

    plt.figure(figsize=(5,3))
    plt.bar(class_names, average_scores, width=0.2)
    plt.xlabel('Class')
    plt.ylabel('Percentage(%)')
    plt.title('Average Performance')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert the plot to a base64 image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')
    plt.close()   

    for subject in teacher.subject.all():
        count_subjects += 1

    list = zip(class_names, average_scores)
    context = {
        'teacher': teacher,
        'count_classes': count_classes,
        'count_subjects': count_subjects,
        'count_students': count_students,
        'list': list,
        'graphic': graphic,
    }
    return render(request, 'teacher/teacher_dashboard.html', context)

@login_required
def view_reports(request):
    student = request.user.student
    reports = Report.objects.filter(student=student)
    return render(request, 'students/reports.html', {'reports': reports})

@login_required
@admin_required
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

@login_required
#@admin_required
def applications_review(request):
    applications = Application.objects.exclude(status = 'completed')
    forms = []
    if request.method == 'POST':
        for application in applications:
            form = ApplicationReviewForm(request.POST, prefix=str(application.id))
            if form.is_valid():
                report = form.save(commit=False)
                if report.status is not None and report.status != application.status:
                    application.status = report.status
                    application.save()
            forms.append(form)
    else:
        forms = [ApplicationReviewForm(prefix=str(application.id)) for application in applications]

    lists = zip(applications, forms)
    return render(request, 'admin/applications_review.html', {'lists':lists})