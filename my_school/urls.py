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
    path('register/', views.register, name='register'),
    #path('login/', views.login_view, name='login'),
    path('logged_out/', views.logout_view, name='logged_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student_dashboard/', views.student_dashboard, name = 'student_dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

