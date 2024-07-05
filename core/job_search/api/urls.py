from django.urls import path
from . import views 
urlpatterns=[
    path('',views.getRoutes),
    path('jobs/',views.getJobs),
    path('jobs/<str:pk>/',views.getJob)
]