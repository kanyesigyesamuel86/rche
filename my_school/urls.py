from django.urls import path
from . import views
from . views import login_page, signup, dashboard, contact, all_users, logout_user

urlpatterns = [
    path('login/', login_page, name = 'login_page'),
    path('signup/', signup, name = 'signup'),
    path('contact/', contact, name= 'contact'),
    path('dashboard/', dashboard, name ='dashboard'),
    path('all_users/', all_users, name = 'all_users'),
    path('logout/', logout_user, name='logout'),

]