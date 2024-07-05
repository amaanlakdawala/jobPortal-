from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render,redirect
from job_search.models import *
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .forms import UserForm
from django.core.mail import send_mail,EmailMultiAlternatives
from django.db.models import Q

# Create your views here.

def home(request):
     if request.user.is_authenticated:
          jobs = Jobs.objects.filter(user=request.user)
          
          context={'jobs':jobs}
          return render (request,'employers/ehome.html',context)
    
         
           
    

def jobs_posted(request):
    jobs = Jobs.objects.all()
    context={'jobs':jobs}
    return render (request,'employers/jobs_posted.html',context)

def register(request):
     return HttpResponse("hello world")

def login_view(request):
     return render (request,'job_search/login.html')

def eprofile(request):
     employers = Employers.objects.all()
     user_organization_name = request.user.organization
     user_organization = Employers.objects.get(organization=user_organization_name)
     print(f"user org {user_organization}")
     job_appilcations = JobApplication.objects.filter(jobs__organization = user_organization).order_by('-appplied_at')
     print(f"jobs application {job_appilcations}")
     
     if request.method == "POST":
         print("inside form")
         user_id = request.POST.get('user_id')
         print(f"user_id {user_id}")
         user = User.objects.get(id = user_id)
         user_email = user.email
         user_name = user.name
         employer_name = request.user.name
         employer_organization = request.user.organization
         print(f"user Name = {user_name}")
         print(f"user Emial = {user_email}")
         print(f"Employer name = {employer_name}")
         subject='Confirmation'
         from_email = 'talenttrovejobs@gmail.com'
         to = f'{user_email}'
         text_content = f"Hey {user_name} this is to inform you that your application have been viewed by the recruiter "
         html_content = f"<p>Hey <strong>{user_name}</strong> this is to inform you that your application have been viewed by the recruiter <strong> {employer_name}</strong> from Company <strong> {employer_organization} </strong></p>"
         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
         msg.attach_alternative(html_content, "text/html")
         msg.send()
         print("email send")
         return redirect ("candidate_description",pk=user_id)
     


     

     




     context={'employers':employers,'job_appilcations':job_appilcations}
     return render(request,'employers/eprofile.html',context)



def e_search_employee(request):
     users = User.objects.filter(is_employee=True)
    
     if request.method=='POST':
          location = request.POST.get('select')  
          print(f"location {location}") 

          experience = request.POST.getlist('experience')
          print(f"experience {experience}")
          if   location and location !='Anywhere':
               users = users.filter(Q(location=location,experience__in=experience))
          else:
               users = users.filter(experience__in=experience)
          
                                 
                                  
           
     if request.GET.get('q'):
        q = request.GET.get('q')
     else:
        q=""
     print(q)
     users = users.filter(Q(skills__icontains=q))

     context={'users':users}
     return render(request,'employers/e_search_employee.html',context)


def candidate_description(request,pk):
     user = User.objects.get(id=pk)
     user_email = user.email
     user_name = user.name
     user_instance = User.objects.get(email=user_email)
     employer = request.user



     if request.method =='POST':
          room_exists = Room.objects.filter(user=user_instance, employer=employer).exists()
          
   
          if room_exists:
               room1 = Room.objects.get(user=user_instance, employer=employer)
               return redirect ('chat',pk=room1.id)
          else:


          
          
               subject='Confirmation'
               from_email = 'talenttrovejobs@gmail.com'
               to = f'{user_email}'
               text_content = f"Hey {user_name} this is to inform you that an hr is interested in your profile "
               html_content = f"<p>Hey <strong>{user_name}</strong> this is to inform you that an hr is interested in your profile.</p>"
               msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
               msg.attach_alternative(html_content, "text/html")
               msg.send()
               
         
               room = Room.objects.create(user = user_instance,employer = employer)
               room.save()
               print("room have been created")
               return redirect ('chat',pk=room.id)
         
     context={'user':user}
     return render (request,'employers/candidate_description.html',context)



def contact(request):
  
    context={}
    if request.method == 'POST':
        query = request.POST.get('query')
        print(query)
        user = request.user

        print(user)
        c = Complaint.objects.create(user = user,body = query)
        c.save()
        messages.success(request, 'Your Message Have Been Delivered And it Will Be Solved Within 24 Hours')
        return redirect('econtact')  
    return render (request,'employers/econtact.html',context)     
    

# def contact(request):
#     form = ComplaintUser()
#     context={'form':form}
#     context ={}
#     return render (request,'employers/econtact.html',context)


def about(request):
    context={}
    return render (request,'employers/eabout.html',context)

def postjob(request):
     if request.method=="POST":
          # names = request.POST.get('name')
          organization = request.POST.get('organization')
          employer,_ = Employers.objects.get_or_create(organization=organization)
         
          role=request.POST.get('role')
          roles,_ = Roles.objects.get_or_create(name = role)

          skill=request.POST.get('skill')
          salary=request.POST.get('salary')
          location=request.POST.get('location')
          vacancy = request.POST.get('vacancy')
          experience = request.POST.get('experience')
          education = request.POST.get('education')
          application_date = request.POST.get('application_date')

          job_type=request.POST.get('job_type')
          job_types,_ = JobType.objects.get_or_create(job_type=job_type)
          
          job = Jobs.objects.create(user = request.user,organization=employer,role=roles,skills=skill,salary=salary,location=location,job_type=job_types,
                                    vacancy=vacancy,experience=experience,education=education,application_date=application_date)
          
          job.save()
          return redirect('epostjob')

     context={}
     return render (request,'employers/epostjob.html',context)

def eupdate(request,pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method=='POST':
        name=request.POST.get('name')
        logo = request.FILES.get('logo')
        video = request.FILES.get('video') 
        about = request.POST.get('about')
        organization = request.POST.get('organization')

        employers = Employers.objects.get(name=user.name)
        employers.name = name
        employers.avatar = logo
        employers.video = video
        employers.about = about
        employers.organization = organization
        employers.save()
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('eprofile')
    context={'form':form}
    return render(request,'employers/eupdate.html',context)


def ejobdescription(request,pk):
      job = Jobs.objects.get(id=pk)  
      user = request.user
      context={'job':job}       
      return render(request,'employers/ejobdescription.html',context)


def candidate_list(request):
     users = User.objects.all()
     context={'users':users}
     return render(request,'employers/e_search_employee.html',context)

def message(request):
     user = request.user
     rooms = Room.objects.filter(employer=user)
     if request.method == 'POST':       
        user_id = request.POST.get('user_id')
        print(user_id)
        if user_id:
            try:
                user1 = User.objects.get(id=user_id)

                print(user.email)
                room = Room.objects.filter(user=user1,employer = request.user)
                print(room)
                room.delete()
                print("Room deleted")
                return redirect('message')  # Redirect to a success page or any other URL
            except Room.DoesNotExist:
                print("Room does not exist")
                # Handle the case where the room does not exist
                return redirect('error_url')  # Redirect to an error page or any other URL
        else:
            print("User not provided")
           


     context = {'rooms':rooms}
     
     return render(request,'employers/messages.html',context)

def chat(request,pk):
     room=Room.objects.get(id=pk)
     room_messages=room.message_set.all()
     
     if request.method=="POST":
          message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')          
        )
          user_email = room.user.email
          user_name = room.user.name
          employer_name = request.user.name
          print(user_email)
          print(user_name)
          subject='Message'
          from_email = 'talenttrovejobs@gmail.com'
          to = f'{user_email}'
          text_content = f"Hey {user_name} this is to inform you that an HR {employer_name} Has Message You "
          html_content = f"<p>Hey <strong>{user_name}</strong> this is to inform you that an HR  {employer_name} Has Message You</p>"
          msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
          msg.attach_alternative(html_content, "text/html")
          msg.send()
          messages.success(request,"Congratulations! An email has been send to Candidate")
       
          return redirect ('chat', pk=room.id)

     context={'room':room,'room_messages':room_messages}

     return render(request,'employers/chat.html',context)






