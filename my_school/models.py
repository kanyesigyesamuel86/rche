
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import RegexValidator
from cities_light.models import Country, City
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage



class CustomUser(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    age = models.CharField(max_length=10, null = True)
    photo = models.ImageField(upload_to='user_photos/', blank=True)
    USER_TYPES = (

        ('headteacher', 'Headteacher'),
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('other', '---'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='other')


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

class Feedback(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now_add=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    announcement = models.ManyToManyField(Announcement)
    tags = TaggableManager()
    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    subject = models.ManyToManyField(Subject)
    announcement = models.ManyToManyField(Announcement)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title

class Attendance(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    def __str__(self):
        return self.status
    
class LibraryBook(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

class BorrowedBook(models.Model):
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)

class Fee(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

class Report(models.Model):
    report_file = models.FileField(upload_to='reports/', null = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.report_file)


# Student models
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,  null=True, blank=True)
    subject = models.ManyToManyField(Subject)
    feedback = models.ManyToManyField(Feedback)
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

class NonStudent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ROLES = {'standard': '---',
        'headteacher': 'Headteacher',
        'deputy_headteacher_academics':'Deputy Headteacher, Administration',
        'deputy_headteacher_academics':'Deputy Headteacher, Academics',
        'deputy_headteacher_welfare_and_co-curricular':'Deputy Headteacher, Co-curricular',
    }
    role = models.CharField(choices = ROLES, max_length = 100, default = None, null= True)
    department = models.CharField(max_length=100)
    qualifications = models.TextField()
    date_of_joining = models.DateField(null=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    next_of_kin = models.CharField(max_length=100)
    relationship = models.CharField( null=True, max_length = 30, choices=[('mother', 'Mother'), ('father', 'Father'), ('child', 'Child'),('relative', 'Relative'),('beneficiary', 'Beneficiary'), ])
    next_of_kin_phone = models.CharField(max_length=15)
    course = models.ManyToManyField(Course)
    subject = models.ManyToManyField(Subject)
    feedback = models.ManyToManyField(Feedback)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"




class Application(models.Model):
    date_applied = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    address = models.CharField(max_length=100)
    city_or_district = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    document_name = models.FileField(upload_to='documents/', max_length=254, null=True, blank=True)
    STATUS_CHOICES = (
        ('review', 'Under Review'),
        ('admitted', 'Admitted'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
@receiver(pre_save, sender=Application)
def send_email_on_admission(sender, instance, **kwargs):
    if instance.status == 'admitted':
        email = EmailMessage(
            "Admission to Ryakasinga CHE",
            "Congratulations! \nYou have been admitted",
            " 'Ryakasinga CHE' <info.ryakasinga@gmail.com>",
            [instance.email],
            reply_to=["kanyesigyesamuel86@gmail.com"],
            headers={"Message-ID": "foo"},
        )
        email.send()
        instance.status = 'completed'
