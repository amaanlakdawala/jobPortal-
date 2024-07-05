from django.contrib import admin
from. models import User,Jobs,Roles,JobType,JobApplication,Employers,Room,Message,Complaint,Payment

# Register your models here.

admin.site.register(User)
admin.site.register(Employers)
admin.site.register(Jobs)
admin.site.register(Roles)
admin.site.register(JobType)
admin.site.register(JobApplication)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Complaint)
admin.site.register(Payment)


