from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
# Create your models here.

class NewUser(AbstractUser):
    class_name = models.CharField(max_length=20, blank= True)
    

class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(NewUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Year(models.Model):
	id = models.AutoField(primary_key=True)
	course_name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Subjects(models.Model):
	id =models.AutoField(primary_key=True)
	subject_name = models.CharField(max_length=255)
	
	# need to give default course
	subject_id = models.ForeignKey(Year, on_delete=models.CASCADE, default=1) 
	staff_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()


class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin = models.OneToOneField(NewUser, on_delete = models.CASCADE)
	gender = models.CharField(max_length=50)
	profile_pic = models.FileField()
	address = models.TextField()
	course_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING, default=1)
	session_year_id = models.ForeignKey(Year, null=True,on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = models.Manager()