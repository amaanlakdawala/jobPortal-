# classes that take python object and convert it into json data
from rest_framework.serializers import ModelSerializer
from job_search.models import Jobs

class JobsSerializer(ModelSerializer):
    class Meta:
        model=Jobs
        fields= '__all__'