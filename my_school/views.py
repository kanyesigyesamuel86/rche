
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Course, Application
from .forms import ApplicationForm, SubjectForm, CourseForm
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, StudentForm, StudentForm2
from . models import Student, Enrollment, Assignment, Attendance, Announcement, LibraryBook, BorrowedBook, Fee, Feedback, Course, CustomUser, NonStudent
from django .views import generic
from django.contrib import messages
from .decorators import hteacher_required, admin_required, teacher_required
from django.contrib.auth.decorators import login_required

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

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Student.objects.create(user=user)
            return redirect('login')
    else:
        form = StudentForm()
    return render(request, 'register.html', {'form': form})

def register_student2(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register_student')

    user = CustomUser.objects.get(username=user_id)
    if request.method == 'POST':
        form = StudentForm2(request.POST, instance=user)
        if form.is_valid():
            form.save(),
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

def dashboard(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    num_visits = request.session['num_visits']

    return render(request, 'dashboard.html', {'num_visits': num_visits})

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

def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)

        enrollments = Enrollment.objects.filter(student=student)
        assignments = Assignment.objects.filter(course__in=enrollments.values_list('course', flat=True))
        attendance = Attendance.objects.filter(student=student)
        announcements = Announcement.objects.all().order_by('-date')[:5]
        borrowed_books = BorrowedBook.objects.filter(student=student)
        fees = Fee.objects.filter(student=student)
        feedbacks = Feedback.objects.filter(student=student)
        
    except Student.DoesNotExist:
        messages.error(request, 'Student profile does not exist.')
        return redirect('dashboard')
    student = Student.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    assignments = Assignment.objects.filter(course__in=enrollments.values_list('course', flat=True))
    attendance = Attendance.objects.filter(student=student)
    announcements = Announcement.objects.all().order_by('-date')[:5]
    borrowed_books = BorrowedBook.objects.filter(student=student)
    fees = Fee.objects.filter(student=student)
    feedbacks = Feedback.objects.filter(student=student)
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'assignments': assignments,
        'attendance': attendance,
        'announcements': announcements,
        'borrowed_books': borrowed_books,
        'fees': fees,
        'feedbacks': feedbacks,
    }
    return render(request, 'student/dashboard.html', context)