
from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render,redirect
from job_search.models import *
from django.contrib.auth import authenticate,login,logout
# from .forms import UserRegistrationForm,UserLoginForm
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
     # else:
     #      return render (request,'employers/elogin.html')
         
           
    

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
     job_appilcations = JobApplication.objects.filter(jobs__organization = user_organization)
     print(f"jobs application {job_appilcations}")
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
               messages.success(request,"Congratulations! An email has been send to Candidate")
         
               room = Room.objects.create(user = user_instance,employer = employer)
               room.save()
               print("room have been created")
               return redirect ('chat',pk=room.id)
         
     context={'user':user}
     return render (request,'employers/candidate_description.html',context)

def contact(request):
#     form = ComplaintUser()
#     context={'form':form}
    context ={}
    return render (request,'employers/econtact.html',context)


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
     #  user_email = request.user.email
     #  user_name = request.user.name
     #  applied=True
     #  if request.method =='POST':
     #    if JobApplication.objects.filter(users=user,jobs=job).exists():
     #        messages.warning(request,"You Have already Applied For Job")
     #        applied = True
     #        print("success")
     #        return redirect('job_description',pk=job.id)
     #    else:
     #        applied=False
     #        job_appilcation  = JobApplication(users = user,jobs=job)
     #        job_appilcation.save()


          #   subject='Confirmation'
          #   from_email = 'talenttrovejobs@gmail.com'
          #   to = f'{user_email}'
          #   text_content = f"Hey {user_name} this is to inform you that your resume have been submitted "
          #   html_content = f"<p>Hey <strong>{user_name}</strong> this is to inform you that your resume have been submitted.</p>"
          #   msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
          #   msg.attach_alternative(html_content, "text/html")
          #   msg.send()

          #   messages.success(request,"Congratulations! Your Application was Submitted to the Recruiter ")
        
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
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                room = Room.objects.get(user=user)
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
       
        return redirect ('chat', pk=room.id)

     context={'room':room,'room_messages':room_messages}

     return render(request,'employers/chat.html',context)






# def jobs(request):
#     user = request.user
#     jobs = Jobs.objects.all()
#     jobs = Jobs.objects.filter(user=user)

    
    
#     # Fetch jobs posted by the logged-in employer
#     employer_jobs = Jobs.objects.filter(organization=employer)
    
#     context = {'jobs': jobs}
#     return render(request, 'employers/ejobs.html', context)

    
#     paginator = Paginator(jobs,1)
#     page_number = request.GET.get('page')
#     finaljobs = paginator.get_page(page_number)


#     context={'jobs':jobs,'user':user}
#     return render(request,'employers/ejobs.html',context)


# class EmployersAuthBackend(object):
#     def authenticate(self, request, email=None, password=None):
#         try:
#             employer = Employers.objects.get(email=email)
#             if employer.check_password(password):
#                 return employer
#         except Employers.DoesNotExist:
#             return None
        

# def login_view(request):
   
#     if request.method=='POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)
#         print(password)
#         try:
#             employer = Employers.objects.get(email=email)
#             print(employer)
#         except:
#             messages.error(request,'User not found')
       
            
#         user = authenticate(request,email=email,password=password)
#         print(user)
#         if user is not None:
#             messages.error(request,'User found')
#             print("user autheticated")
#             login(request,user)
#             return redirect('ehome')
#         else:
#             print("not found")
#             messages.error(request,'Email or Password is incorrect')   
#     context={}
#     return render (request,'employers/elogin.html',context)






# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         user = authenticate(request, email=email, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             return redirect('ehome')  # Redirect to home page after successful login
#         else:
#             print("Some error occurred")
#             return render(request, 'employers/elogin.html')
#     else:
#         return render(request, 'employers/elogin.html')

# # Implement logout view
# def logout_view(request):
#     logout(request)
#     return redirect('login') 



# def register(request):
#     form = UserRegistrationForm()
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.email = user.email.lower()
#             user.save()
#             login(request, user)
#             return redirect('eloginPage')
#         else:
#             messages.error(request, "Some error occurred")
#     return render(request, 'employers/eregister.html', {'form': form})


# def login_view(request):
    
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print("Received email:", email)  
#         print("Received password:", password) 
#         try:
#             user = Employers.objects.get(email=email)
#             print(user)
#         except:
#             messages.error(request,'User not found')

#         user = authenticate(request,email=email,password=password)
#         print(user)
#         if user is not None:
#             login(request,user)
#             return redirect('ehome')
#         else:
#             messages.error(request,'Email or Password is incorrect')   
#     context={}
#     return render (request,'employers/elogin.html',context)

       
#         user = authenticate(request, email=email, password=password)
#             print(user)
#             if user is not None:
#                 login(request, user)
#                 return redirect('ehome')  # Redirect to home page after successful login
#             else:
#                 messages.error(request, 'Invalid email or password.')
#     return render(request, 'employers/elogin.html', {'form': form})





