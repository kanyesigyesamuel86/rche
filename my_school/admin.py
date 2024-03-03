from django.contrib import admin
from .models import Course, Student, Application, Subject, CustomUser

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Application)
admin.site.register(CustomUser)
