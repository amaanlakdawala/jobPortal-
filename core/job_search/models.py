from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from .manager import UserManager
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    cv = models.FileField(null=True,blank=True)
    avatar = models.ImageField(null=True,default='avatar.svg')
    skills = models.CharField(max_length=1000,null=True,blank=True)
    complaints = models.TextField(null=True,blank=True)
    experience = models.CharField(max_length=100, default='1 Years')
    education = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    about = models.CharField(max_length=1000,null=True,blank=True)
    video = models.FileField(null=True,blank=True) 
    logo = models.ImageField(null=True,default='avatar.svg')
    organization = models.CharField(null=True,blank=True,max_length=100)
     
   

    

    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
   
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.email




class Employers(models.Model):
   
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100,null=True,blank=True)
    avatar = models.ImageField(null=True,default='avatar.svg')
    about = models.CharField(max_length=1000,null=True,blank=True)
    video = models.FileField(null=True,blank=True)   

   
    def __str__(self):
         if self.organization:
            return self.organization
         else:
            return self.name
        
         
            
     
    


class Roles(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class JobType(models.Model):
    job_type = models.CharField(max_length=100, default='Full-Time')

    def __str__(self):
        return self.job_type


class Jobs(models.Model):
    name = models.CharField(max_length=100, null=True, default='Not Disclosed',blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    job_type = models.ForeignKey(JobType,on_delete=models.CASCADE)
    organization = models.ForeignKey(Employers,on_delete=models.CASCADE)
    role = models.ForeignKey(Roles,on_delete=models.SET_NULL,null=True,blank=True)
    skills = models.CharField(max_length=100,blank=False,null=False)
    salary = models.TextField(max_length=100,default='Not Disclosed')
    location = models.CharField(max_length=100,null=True,blank=True)
    education = models.CharField(max_length=1000,null=True)
    experience = models.CharField(max_length=1000,null=True)
    vacancy = models.PositiveIntegerField(null=True)
    application_date = models.DateField(null=True)

    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
         if self.role:
            return str(self.role)
         


class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contacted_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} Contacted"

    
            
         
           
       
    
   
    

class JobApplication(models.Model):
    users = models.ForeignKey(User,on_delete=models.CASCADE)
    jobs = models.ForeignKey(Jobs,on_delete=models.CASCADE)
    appplied_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('users','jobs')

    def __str__(self):
        return f"{self.users.name} Applied For {self.jobs.role}"
    

class Room(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL ,null=True)
    employer = models.ForeignKey(User, on_delete=models.SET_NULL ,related_name='employer',null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','employer')

        ordering=['-updated','-created']

   
    


    
class Message(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField()
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    
    created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['created']

    def __str__(self):
        return self.body[0:50]


    
class Complaint (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
     
    class Meta:
        ordering=['created']

    def __str__(self):
        return f"Complaint from {self.user} is  {self.body [0:50]}"
    

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)

    def __str__(self):
        return f"payment done by {self.user}"


        


