from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='ehome'),
    path('eregister/',views.register,name='eregister'),
    path('eloginPage/',views.login_view,name='eloginPage'),
    path('e_search_employee/',views.e_search_employee,name='e_search_employee'),
    path('eprofile/',views.eprofile,name='eprofile'),
    path('eabout/',views.about,name='eabout'),
    path('econtact/',views.contact,name='econtact'),
    path('epostjob/',views.postjob,name='epostjob'),
    path('eupdate/<int:pk>/',views.eupdate,name='eupdate'),
    path('ejobdescription/<int:pk>/',views.ejobdescription,name='ejobdescription'),
    path('candidate_description/<int:pk>/',views.candidate_description,name='candidate_description'),
 
   
    
    path('message/',views.message,name='message'),
    path('chat/<int:pk>/',views.chat,name='chat'),


   

]