from django.http import JsonResponse #to provide response as jsom
from rest_framework.decorators import api_view
from rest_framework.response import Response
from job_search.models import Jobs
from .serializers import JobsSerializer
@api_view(['GET']) #methods we can specify user can opnly get data
def getRoutes(request): #will show all routes in api
    routes=[
        'Get /api'
        'Get /api/jobs',
        'Get /api/jobs/:id'
    ]
    
    return Response(routes) #safe qwill alow to turn python list to json list

@api_view(['GET'])
def getJobs(request):
    jobs = Jobs.objects.all()
    serializer = JobsSerializer(jobs,many=True) #are there going to be many objects to serialize
    return Response(serializer.data)

@api_view(['GET'])
def getJob(request,pk):
    job = Jobs.objects.get(id=pk)
    serializer = JobsSerializer(job,many=False) #are there going to be many objects to serialize
    return Response(serializer.data)