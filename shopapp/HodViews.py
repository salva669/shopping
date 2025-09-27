from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum, Avg 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from shopapp.models import CustomUser, Staffs, Courses, Subjects, Bidhaas, FeedBackStaffs, \
    LeaveReportStaff
from .forms import AddBidhaaForm, EditBidhaaForm, SearchBidhaaForm, BulkUpdateQuantityForm

def admin_home(request):
    bidhaa_count=Bidhaas.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    bidhaa_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        bidhaas=Bidhaas.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        bidhaa_count_list_in_course.append(bidhaas)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    bidhaa_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        bidhaa_count=Bidhaas.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        bidhaa_count_list_in_subject.append(bidhaa_count)

    staffs=Staffs.objects.all()
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        staff_name_list.append(staff.admin.username)

    bidhaas_all=Bidhaas.objects.all()
    bidhaa_name_list=[]
    for bidhaa in bidhaas_all:
        bidhaa_name_list.append(bidhaa.jina)


    return render(request,"hod_template/home_content.html",{"bidhaa_count":bidhaa_count,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"bidhaa_count_list_in_course":bidhaa_count_list_in_course,"bidhaa_count_list_in_subject":bidhaa_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list})

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(
                reverse("add_staff")
                )
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(
                reverse("add_staff")
                )

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

@login_required
def add_bidhaa(request):
    #view to add new bidhaa
    if request.method == 'POST':
        form = AddBidhaaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                bidhaa = form.save()
                messages.success(request, f'Successfully added "{bidhaa.jina}"')
                return redirect('manage_bidhaa')
            except Exception as e:
                messages.error(request, f'Error adding bidhaa: {str(e)}')
        
        else:
            messages.error(request, 'Please correct the errors below')

    else:
        form=AddBidhaaForm()

    context = {
        'form': form,
        'page_title': 'Add New Bidhaa',
        'button_text': 'Add Bidhaa',
        'action_url': reverse('add_bidhaa')
    }

    #return render(request,"hod_template/add_bidhaa_template.html",{"form":form})
    return render(request,"hod_template/add_bidhaa_template.html", context)

def add_bidhaa_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddBidhaaForm(request.POST, request.FILES)
        if form.is_valid():
            jina = form.cleaned_data["jina"]
            category = form.cleaned_data["category"]
            brand = form.cleaned_data["brand"]
            quantity = form.cleaned_data["quantity"]
            alert_quantity = form.cleaned_data["alert_quantity"]
            price = form.cleaned_data["price"]
            code = form.cleaned_data["code"]
            profile_pic = request.FILES['profile_pic']

            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                bidhaa = Bidhaas(
                    jina=jina,
                    category=category,
                    brand=brand,
                    quantity=quantity,
                    alert_quantity=alert_quantity,
                    price=price,
                    code=code,
                    profile_pic=profile_pic_url
                )
                bidhaa.save()

                messages.success(request, "Successfully Added Bidhaa")
                return HttpResponseRedirect(reverse("add_bidhaa"))
            except Exception as e:
                messages.error(request, f"Failed to Add Bidhaa: {e}")
                return HttpResponseRedirect(reverse("add_bidhaa"))
        else:
            return render(
                request,
                "hod_template/add_bidhaa_template.html",
                {"form": form}
            )


def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(
                reverse("add_subject")
                )
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(
                reverse("add_subject")
                )

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

@login_required
def manage_bidhaa(request):
    #view to display and search all bidhaa
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    low_stock_only = request.GET.get('low_stock_only', False)

    #Base queryset
    bidhaas = Bidhaas.objects.all().order_by('-created_at')

    #Apply search filters
    if search_query:
        bidhaas = bidhaas.filter(
            Q(jina_icontains=search_query) |
            Q(category_icontains=search_query) |
            Q(brand_icontains=search_query) |
            Q(code_icontains=search_query) 
        )
    
    if category_filter:
        bidhaas = bidhaas.filter(
            category_icontains=category_filter
        )

    if min_price:
        try:
            bidhaas = bidhaas.filter(
                price_gte=float(min_price)
                )
        except ValueError:
            pass

    if max_price:
        try:
            bidhaas = bidhaas.filter(
                price_lte=float(max_price)
                )
        except ValueError:
            pass

    if low_stock_only:
        #show items where quantity <= alert quantity
        bidhaas = bidhaas.filter(
            quantity_lter=models.F('alert_quantity')
            )

    #Pagination
    paginator = Paginator(bidhaas, 10) # show 10 bidhaa per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'bidhaas': page_obj,
        'search_form': SearchBidhaaForm(request.GET),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
    }

    #return render(request,"hod_template/manage_bidhaa_template.html",{"bidhaas":bidhaas})
    return render(request,"hod_template/manage_bidhaa_template.html", context)

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

@login_required
def edit_bidhaa(request, bidhaa_id):
    #view to edit existing bidhaa
    bidhaa = get_object_or_404(Bidhaas, id=bidhaa_id)
    
    if request.method == 'POST':
        form = EditBidhaaForm(request.POST, request.FILES, instance=bidhaa)
        if form.is_valid():
            try:
                updated_bidhaa = form.save()
                messages.success(request, f'Successfully updated "{updated_bidhaa.jina}"')
                return redirect('manage_bidhaa')
            
            except Exception as e:
                messages.error(request, f'Error updating bidhaa: {str(e)}')

        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = EditBidhaaForm(instance=bidhaa)

    context = {
        'form': form,
        'bidhaa': bidhaa,
        'page_title': f'Edit {bidhaa.jina}',
        'button_text': 'Update Bidhaa',
        'action_url': reverse('edit_bidhaa', kwargs={'bidhaa_id': bidhaa_id})
    }  

    return render(request, "hod_template/edit_bidhaa_template.html", context)


def edit_bidhaa_save(request, bidhaa_id):
    bidhaa = get_object_or_404(Bidhaas, id=bidhaa_id)

    if request.method != "POST":
        messages.error(request, "Invalid request method")
        return redirect("edit_bidhaa", bidhaa_id=bidhaa.id)

    form = EditBidhaaForm(request.POST, request.FILES, instance=bidhaa)

    if form.is_valid():
        form.save()
        messages.success(request, "Bidhaa updated successfully")
        return redirect("edit_bidhaa", bidhaa_id=bidhaa.id)
    else:
        messages.error(request, "Failed to update bidhaa. Please check the form.")
        return render(request, "hod_template/edit_bidhaa_template.html", {
            "form": form,
            "id": bidhaa.id,
            "jina": bidhaa.jina,
        })



def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")
        try:
            course=Courses.objects.get(id=course_id)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

@login_required
def view_bidhaa(request, bidhaa_id):
    #view to display detailed bidhaa information
    bidhaa = get_object_or_404(Bidhaas, id=bidhaa_id)

    #check if stock is low
    is_low_stock = bidhaa.quantity <= bidhaa.alert_quantity

    context = {
        'bidhaa': bidhaa,
        'is_low_stock': is_low_stock,
        'page_title': f'View {bidhaa.jina}'
    }

    return render(request, 'hod_template/view_bidhaa_template.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def delete_bidhaa(request, bidhaa_id):
    #View to delete bidhaa
    bidhaa = get_object_or_404(Bidhaas, id=bidhaa_id)

    if request.method == 'POST':
        bidhaa_name = bidhaa.jina
        try:
            bidhaa.delete()
            messages.success(request, f'Successfully deleted "{bidhaa_name}"')
        
        except Exception as e:
            messages.error(request, f'Error deleting bidhaa: {str(e)}')

        return redirect('manage_bidhaa')

    context = {
        'bidhaa': bidhaa,
        'page_title': f'Delete {bidhaa.jina}'
    }

    return render(request, 'hod_template/delete_bidhaa_template.html', context)
    
@login_required
def bulk_update_quantities(request):
    #view to bulk update bidhaa quantities
    if request.method == 'POST':
        #get selected bidhaa IDs
        selected_ids = request.POST.getlist('selected_bidhaas')

        if not selected_ids:
            messages.error(request, 'No bidhaa selected')
            return redirect('manage_bidhaa')

        bidhaas = Bidhaas.objects.filter(id__in=selected_ids)
        form = BulkUpdateQuantityForm(request.POST, bidhaas=bidhaas)

        if form.is_valid():
            updated_count = 0

            for bidhaa in bidhaas:
                field_name = f'quantity_{bidhaa.id}'

                if field_name in form.cleaned_data:
                    new_quantity = form.cleaned_data[field_name]
                    if new_quantity != bidhaa.quantity:
                        bidhaa.quantity = new_quantity
                        bidhaa.save()
                        updated_count += 1

            if updated_count > 0:
                messages.success(request, f'Successfully updated {updated_count} bidhaa quantities')

            else:
                messages.info(request, 'No quantities were changed')

            return redirect('manage_bidhaa')
        
    else:
        #GET request - show form
        selected_ids = request.GET.getlist('ids')
        
        if not selected_ids:
            messages.error(request, 'No bidhaa selected')
            return redirect('manage_bidhaa')
    
        bidhaas = Bidhaas.objects.filter(id__in=selected_ids)
        form = BulkUpdateQuantityForm(bidhaas = bidhaas)

    context = {
        'form': form,
        'bidhaas': bidhaas,
        'page_title': 'Bulk Update Quantities'
    }

    return render(request, 'hod_template/bulk_update_quantities_template.html', context)

@login_required
def low_stock_alert(request):
    #view to show bidhaa with low stock
    low_stock_bidhaas = Bidhaas.objects.filter(
        quantity__lte = models.F('alert_quantity')
    ) .order_by('quantity')

    paginator = Paginator(low_stock_bidhaas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'bidhaas': page_obj,
        'page_title': 'Low Stock Alert',
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'paginator': paginator,
    }

    return render(request, 'hod_template/low_stock_alert_template.html', context)

@login_required
def bidhaa_statistics(request):
    #view to show bidhaa statistics
    stats = {
        'total_bidhaas': Bidhaas.objects.count(),
        'total_value': Bidhaas.objects.aggregate(
            total = Sum(models.F('quantity') * models.F('price'))
        )['total'] or 0,
        'low_stock_count': Bidhaas.objects.filter(
            quantity__lte = models.F('alert_quantity')
        ).count(),
        'average_price': Bidhaas.objects.aggregate(avg_price = Avg('price'))['avg_price'] or 0,
        'categories_count': Bidhaas.objects.values('category').distinct().count(),
        'brands_count': Bidhaas.objects.values('brand').distinct().count(),
    }

    #top categories by count
    top_categories = Bidhaas.objects.values('category').annotate(
        count = Count('id')
    ) .order_by('-count')[:5]

    #top brands by count
    top_brands = Bidhaas.objects.values('brand').annotate(
        count = Count('id')
    ) .order_by('-count')[:5]

    context = {
        'stats': stats,
        'top_categories': top_categories,
        'top_brands': top_brands,
        'page_title': 'Bidhaa Statistics'
    }

    return render(request, 'hod_template/bidhaa_statistics_template.html', context)

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_send_notification_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/staff_notification.html",{"staffs":staffs})

@csrf_exempt
def send_staff_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    staff=Staffs.objects.get(admin=id)
    token=staff.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"bidhaa Management System",
            "body":message,
            "click_action":"https://bidhaamanagementsystem22.herokuapp.com/staff_all_notification",
            "icon":"http://bidhaamanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStaffs(staff_id=staff,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
