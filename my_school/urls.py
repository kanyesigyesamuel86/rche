from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home, name = 'home' ),
    path('populate/', views.populate_database, name='populate'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
    path('apply/<int:course_id>/', views.apply_course, name='apply'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('status/<int:application_id>/', views.application_status, name='status'),
    path('registration', views.registration, name='registration'),
    path('register_staff', views.signup, name = 'register'),
    path('register_staff_2', views.register_non_student_2, name = 'register_staff_2'),
    path('register_student', views.register_student, name = 'register_student'),
    path('register1', views.register_student2, name = 'register1'),
    path('logged_out/', views.logout_view, name='logged_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student_dashboard/', views.student_dashboard, name = 'student_dashboard'),
    path('access_denied', views.access_denied, name = 'access_denied'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_complete/', views.account_activation_complete, name='account_activation_complete'),
    path('teacher_dashboard', views.teacher_dashboard, name = 'teacher_dashboard'),
    path('account_info', views.account_info, name = 'account_info'),
    path('reports', views.reports, name = 'reports') ,
    path('upload_reports/<int:course_id>/', views.upload_reports, name='upload_reports'),
    path('applications_review', views.applications_review, name = 'applications_review'),
    path('class_details/<int:course_id>/', views.apply_course, name='class_details'),
    path('calendar', views.calendar_context, name = 'calendar')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

