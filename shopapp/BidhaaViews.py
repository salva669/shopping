from django.shortcuts import render
import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from shopapp.models import Bidhaas, Courses, Subjects, CustomUser

def bidhaa_home(request):
    bidhaa_obj=Bidhaas.objects.get(admin=request.user.id)
    course=Courses.objects.get(id=bidhaa_obj.course_id.id)
    subjects=Subjects.objects.filter(course_id=course).count()
    subjects_data=Subjects.objects.filter(course_id=course)
    
    subject_name=[]
    subject_data=Subjects.objects.filter(course_id=bidhaa_obj.course_id)
    for subject in subject_data:
        subject_name.append(subject.subject_name)

    return render(request,"bidhaa_template/bidhaa_home_template.html",{"subjects":subjects,"data_name":subject_name})

def bidhaa_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    bidhaa=Bidhaas.objects.get(admin=user)
    return render(request,"bidhaa_template/bidhaa_profile.html",{"user":user,"bidhaa":bidhaa})

def bidhaa_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("bidhaa_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            bidhaa=Bidhaas.objects.get(admin=customuser)
            bidhaa.address=address
            bidhaa.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("bidhaa_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("bidhaa_profile"))