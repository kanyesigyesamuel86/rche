from django.contrib import admin
from .models import CustomUser, Student, Course, Subject, Enrollment, Assignment, Attendance, Announcement, LibraryBook, BorrowedBook, Fee, Feedback, Application, NonStudent

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Attendance)
admin.site.register(Announcement)
admin.site.register(LibraryBook)
admin.site.register(BorrowedBook)
admin.site.register(Fee)
admin.site.register(Feedback)
admin.site.register(Application)
admin.site.register(NonStudent)