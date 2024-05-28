from django.shortcuts import render,redirect
from . models import User,JobApplication,Jobs,JobType,Roles,Room,Message,Complaint
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserForm,UserRegistrationForm,ComplaintUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.conf import settings
import os 
import pdfkit
from docx import Document
import warnings
from io import BytesIO
from django.core.mail import send_mail,EmailMultiAlternatives
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Q
import razorpay

# Create your views here.

def home(request):

    roles = Roles.objects.all()
    user = User.objects.all()
    
    # send_mail(
    #     'Test',
    #     'Message',
    #     'talenttrovejobs@gmail.com',
    #     ['amaanlakdawala301@gmail.com'],
    #     fail_silently=False
    # )

    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q=""
    print(q)
    jobs = Jobs.objects.filter(role__name__icontains=q)
    print(jobs)
    today = timezone.now().date()
    jobs_to_delete = today-timedelta(days=30)
    deleted = Jobs.objects.filter(created__lt = jobs_to_delete)
    deleted.delete()
    paginator = Paginator(jobs,2)
    page_number = request.GET.get('page')
    finaljobs = paginator.get_page(page_number)
    totalpages = finaljobs.paginator.num_pages
    context={'jobs':jobs,'roles':roles,'user':user,'finaljobs':finaljobs,
             'totalpage':[n+1 for n in range(totalpages)]
             
             }
    return render(request,'job_search/home.html',context)

def roles(request):
    jobs = Jobs.objects.all()
    roles = Roles.objects.all()
    job_count = jobs.count()
    context={'roles':roles,'job_count':job_count}
    return render(request,'job_search/home.html',context)

def jobs(request):
    user = User.objects.all()
    jobs = Jobs.objects.all()
    paginator = Paginator(jobs,5)
    page_number = request.GET.get('page')
    finaljobs = paginator.get_page(page_number)

    context={'jobs':jobs,'user':user,'finaljobs':finaljobs}
    return render(request,'job_search/jobs.html',context)

@login_required(login_url='loginPage')
def job_description(request,pk):
    job = Jobs.objects.get(id=pk)  
    user = request.user
    user_email = request.user.email
    user_name = request.user.name
    applied=True
    if request.method =='POST':
        if JobApplication.objects.filter(users=user,jobs=job).exists():
            messages.warning(request,"You Have already Applied For Job")
            applied = True
            print("success")
            return redirect('job_description',pk=job.id)
        else:
            applied=False
            job_appilcation  = JobApplication(users = user,jobs=job)
            job_appilcation.save()


            subject='Confirmation'
            from_email = 'talenttrovejobs@gmail.com'
            to = f'{user_email}'
            text_content = f"Hey {user_name} this is to inform you that your resume have been submitted "
            html_content = f"<p>Hey <strong>{user_name}</strong> this is to inform you that your resume have been submitted.</p>"
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("email send")

            messages.success(request,"Congratulations! Your Application was Submitted to the Recruiter ")
        
    context={'job':job,'applied':applied}       
    return render(request,'job_search/job_description.html',context)



 


 
def job_listing(request): 
    jobs = Jobs.objects.all() 
    
    if request.method=='POST':
        job_types = request.POST.getlist('job_type')       
        location = request.POST.get('select')   
        experience = request.POST.getlist('experience')
        created = request.POST.getlist('created')
        salary = request.POST.get('max_salary')
       
        if 'All'  not in job_types:  
            job_type_instances = JobType.objects.filter(job_type__in=job_types)   
            print(job_type_instances)   
            jobs = Jobs.objects.filter(job_type__in = job_type_instances) 

        if   location and location !='Anywhere':
            jobs = jobs.filter(location=location,experience__in=experience)      
            print(jobs)  

        if created and 'Any' not in created:
            today = timezone.now().date()
            start_date = None
    
            for option in created:
                if option == 'Today':
                    start_date = today
                elif option == 'Last 2 days':
                    start_date = today - timedelta(days=2)
                elif option == 'Last 3 days':
                    start_date = today - timedelta(days=3)
                elif option == 'Last 5 days':
                    start_date = today - timedelta(days=5)
                elif option == 'Last 10 days':
                    start_date = today - timedelta(days=10)

            if start_date is not None:
                 jobs = jobs.filter(created__gte=start_date)

        
        # if 'Any' not in created:
        #     today = timezone.now().date()
        #     print(today)
        #     today = timezone.now().date()
        #     for option in created:
        #         if option == 'Today':
        #             start_date = today
        #         elif option == 'Last 2 days':
        #             start_date = today - timedelta(days=2)
        #         elif option == 'Last 3 days':
        #             start_date = today - timedelta(days=3)
        #         elif option == 'Last 5 days':
        #             start_date = today - timedelta(days=5)
        #         elif option == 'Last 10 days':
        #             start_date = today - timedelta(days=10)
        #     jobs = Jobs.objects.filter(created__gte=start_date)

        if salary !='0':
            jobs = jobs.filter(salary__lte=salary)
            print(jobs)

    if request.GET.get('q'):
        q = request.GET.get('q')
    else:
        q=""
    print(q)
    jobs = jobs.filter(Q(role__name__icontains=q))


    paginator = Paginator(jobs,5)
    page_number = request.GET.get('page')
    finaljobs = paginator.get_page(page_number)
    totalpages = finaljobs.paginator.num_pages
        


           
    context={'jobs':jobs,'finaljobs':finaljobs,
             'totalpage':[n+1 for n in range(totalpages)],
             }   
    return render(request,'job_search/job_listing.html',context)




def register(request):
    form = UserRegistrationForm()
    context = {'form':form}
    if request.method=='POST':
        form =UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            
            login(request,user)
            return redirect('loginPage')
        else:
            messages.error(request,"Some error occurred")
    return render(request,'job_search/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return render(request, 'job_search/login.html')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_employer:
                login(request, user)
                return redirect('ehome')
            elif user.is_employee:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Email or Password is incorrect')
            return render(request, 'job_search/login.html')

    return render(request, 'job_search/login.html')


def change_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        print(email)
        print(new_password)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("User does not exist")

        # Set the new password
        user.set_password(new_password)
        
        # Save the user object to update the password
        user.save()

        return redirect('loginPage')

    return render(request, 'job_search/change_password.html')




# def loginPage(request):
#     error  =None
   

#     if request.method=='POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         try:
#             user = User.objects.get(email=email)
#         except:
#             messages.error(request,'User not found')
#             error = 'User not found'
#         print(" authenticate")
#         user = authenticate(request,email=email,password=password)
#         print("in authenticate")
#         if user is not None and user.is_employer:
#             print("authenticated")
#             login(request,user)
#             print("logges in")
#             return redirect('ehome')
#         elif user is not None and  user.is_employee:
            
#             login(request,user)
#             return redirect('home')

#         else:
#             messages.error(request,'Email or Password is incorrect') 
#             error = 'Email or Password is incorrect'  
#     context={}
#     return render (request,'job_search/login.html',context,error)




def logoutPage(request):
    logout(request)
    return redirect('loginPage')


def profile(request):
    roles = Roles.objects.all()
    job_appilcations =  JobApplication.objects.filter(users=request.user)
    context={'roles':roles,'job_appilcations':job_appilcations}
    return render(request,'job_search/profile.html',context)

@login_required(login_url='loginPage')
def update_profile(request,pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method=='POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'job_search/update_profile.html',context)

def contact(request):
    form = ComplaintUser()
    context={'form':form}
    if request.method == 'POST':
        query = request.POST.get('query')
        print(query)
        user = request.user

        print(user)
        c = Complaint.objects.create(user = user,body = query)
        c.save()
        messages.success(request, 'Your Message Have Been Delivered And it Will Be Solved Within 24 Hours')
        return redirect('contact')

       
        
    return render (request,'job_search/contact.html',context)


def about_us(request):
    context={}
    return render (request,'job_search/about.html',context)


def message(request):
     user = request.user
     rooms = Room.objects.filter(user=user)
     context = {'rooms':rooms}     
     return render(request,'job_search/umessages.html',context)


def chat(request,pk):
     room=Room.objects.get(id=pk)
     room_messages=room.message_set.all()
     
     if request.method=="POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')          
        )
       
        return redirect ('uchat', pk=room.id)

     context={'room':room,'room_messages':room_messages}

     return render(request,'job_search/uchat.html',context)

# def makepayment(request):
#     context = {}
    # o = Order.objects.filter(uid =request.user.id )
    # sum = 0
    # for i in o:
    #     sum = sum + i.pid.price*i.quantity
    #     oid = i.order_id
    # context['sum'] = 1000     
    # client = razorpay.Client(auth=("rzp_test_mv5IZmGRDYEyR3", "NsZOUKGdQeR9SIAAN26TyE8D"))
    # data = { "amount": sum, "currency": "INR", "receipt": 120 }
    # payment = client.order.create(data=data)
    # print(payment)   
    # return render (request,"payment.html",context)


def makepayment(request):
    context = {}
    total = 50000  # Total amount in INR
    amount_in_paise = total * 100  # Convert to paise for Razorpay

    context['total'] = amount_in_paise  # Pass the amount in paise to the template
    
    client = razorpay.Client(auth=("rzp_test_mv5IZmGRDYEyR3", "NsZOUKGdQeR9SIAAN26TyE8D"))
    data = {"amount": amount_in_paise, "currency": "INR", "receipt": "5000"}

    payment = client.order.create(data=data)
    context['payment'] = payment
        
    return render(request, 'job_search/payment.html', context)

# def makepayment(request):
#     context = {}
#     total = 50000
#     context['total'] = total *100
    
#     client = razorpay.Client(auth=("rzp_test_mv5IZmGRDYEyR3", "NsZOUKGdQeR9SIAAN26TyE8D"))
#     data = { "amount": total, "currency": "INR", "receipt": "5000" }

#     payment = client.order.create(data=data)
#     print(payment)   

        
      

#     context['payment'] = payment
        
        
   
 
        
#     return render (request,'job_search/payment.html')

def success_payment(request):
    user_name = "Amaan"
    user_email = 'amaanlakdawala301@gmail.com'      
    subject = 'Payment'
    from_email = 'talenttrovejobs@gmail.com'
    to = f'{user_email}'
    text_content = f"Hey {user_name}, this is to inform you that Your Payment Has Been Processed"
    html_content = f"<p>Hey <strong>{user_name}</strong>, this is to inform you that Your Payment Has Been Processed</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return render (request,'job_search/success_payment.html')
        
    
