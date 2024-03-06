
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('headteacher', 'Headteacher'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='standard')


# Student models
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

class NonStudent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    qualifications = models.TextField()
    date_of_joining = models.DateField(null=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

class LibraryBook(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

class BorrowedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

class Application(models.Model):
    date_applied = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city_or_District = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender_choices = (
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    document_name = models.FileField(upload_to='documents/', max_length=254, default='')

    def __str__(self):
        return f"{self.first_name} "
