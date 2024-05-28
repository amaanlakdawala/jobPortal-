from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    # path('roles/',roles,name='roles'),
    # path('jobs/',jobs,name='jobs'),
    path('job_description/<int:pk>/',job_description,name='job_description' ),
    path('job_listing/',job_listing,name='job_listing'),
    path('register/',register,name='register'),
    path('loginPage/',loginPage,name='loginPage'),
    path('profile/',profile,name='profile'),
    path('update_profile/<int:pk>/',update_profile,name='update_profile'),
    path('contact/',contact,name='contact'),
    path('about_us/',about_us,name='about_us'),
    path('umessage/',message,name='umessage'),
    path('chat/<int:pk>/',chat,name='uchat'),
    path('payment/',makepayment,name='payment'),
    path('success_payment/',success_payment,name='success_payment'),
    
    path('change_password',change_password,name='change_password'),

    # path('resume_viewer/<int:pk>/', resume_viewer, name='resume_viewer'),

]