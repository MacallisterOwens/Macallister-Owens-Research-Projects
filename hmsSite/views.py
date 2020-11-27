from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.shortcuts import render
from hmsSite.models import Project
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date

from .forms import ProjectSubmissionForm, PhemeLoginForm, StillRelevantForm
import random
import os
# Create your views here.

# The home page
def index_view(request,*args, **kwargs):
    def approved_filter(object):
        return object.approved
 
    '''Sort by'''
    order = request.GET.get('sort_by')
    if(order and order != "default"):
        if order == "title_AtoZ":
            option = Lower("title")
        elif order == "title_ZtoA":
            option = Lower('title').desc()
        elif order == "start_date_newest":
            option = '-start_date'
        elif order == "start_date_oldest":
            option = "start_date" 
        elif order == "end_date_newest":
            option = '-end_date'
        elif order == "end_date_oldest":
            option = "end_date" 
    else:
        order = "default"
        option ="-id"

    ''''''
    objs = Project.objects.all().order_by(option)
    approved_projects = filter(approved_filter, objs)
    ''' Paginating''' 

    if request.method == "GET":
        paginator = Paginator(list(approved_projects),10)
        page_num = request.GET.get('page')
    
        try:
            # Get objects on page_num
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # Return the 1st page iff the page num is not integer
            page_obj = paginator.page(1)
        except InvalidPage:
            return HttpResponseNotFound("Error: Page number not found")
        except EmptyPage:
            # Return the last page iff the requested page is out of bound
            page_obj = paginator.page(paginator.num_pages)

    randomlist = random.sample(range(1, len(objs) ), 3)
    randomlist_object_1 = objs.filter(id=randomlist[0])
    randomlist_object_2 = objs.filter(id=randomlist[1])
    randomlist_object_3 = objs.filter(id=randomlist[2])
    carousel_context = {
        'objects_index': page_obj ,
        'random_object_1' : randomlist_object_1,
        'random_object_2' : randomlist_object_2,
        'random_object_3' : randomlist_object_3,
    }
    return render(request,"index.html",carousel_context)

def error_403_view(request, exception):
    return render(request, "error_403.html", exception)

def error_404_view(request, exception):
    return render(request, "error_404.html", exception)

def error_500_view(request):
    return render(request, "error_500.html")

def pheme_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    next_page = request.GET.get('next')
    logon = PhemeLoginForm()
    if request.method == 'POST':
        logon = PhemeLoginForm(request.POST)
        next_page = request.POST.get('next')
        if logon.is_valid():
            # pass the details to auth.py
            user = auth.authenticate(username=logon.cleaned_data['pheme_number'], password=logon.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                if next_page is not None and next_page != "None":
                    return HttpResponseRedirect(next_page)
                elif user.is_staff:
                    return HttpResponseRedirect('/admin')
                else:
                    return HttpResponseRedirect('/')
            else:
                logon.add_error(None, ValidationError('Login unsuccessful', code='login'))
    return render(request, "login.html", { 'form' : logon , 'next' : next_page})

def logout(request, *args, **kwargs):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def addProject_view(request,*args, **kwargs):
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save_form()
            form.save_m2m()
            schoolAdminGroup = str(project.school) + ' Admins'
            relevantUsers = User.objects.filter(Q(groups__name__exact=schoolAdminGroup) | Q(is_superuser=True))
            reversedUrl = ''
            if os.environ.get('DJANGO_ENV') == 'production':
                reversedUrl = f'https://researchprojectsdemo.azurewebsites.net/admin/hmsSite/project/{project.id}/change/'
            else:
                reversedUrl = f'http://127.0.0.1:8000/admin/hmsSite/project/{project.id}/change/'
            for user in relevantUsers:
                user.email_user(
                    'A new project - ' + str(project.title) + ' - has been added by ' + str(project.user.get_full_name()),
                    'Hello ' + user.get_full_name() + ',\r\n\r\nA new project - ' + str(project.title) + ' - has been added by ' + 
                    str(project.user.get_full_name()) + '. Please review this project at your earliest convenience at ' + reversedUrl + '.\r\n\r\nThis is an automated email. Please do not reply to it.',
                    ''
                )
            project.user.email_user(
                f'Your project - {project.title} - is awaiting approval',
                f'Hello {project.user.get_full_name()},\r\n\r\nYour project has been submited and is awaiting approval by a moderator.\r\n\r\nThis is an automated email. Please do not reply to it.',
                ''
            )

            return HttpResponseRedirect('/')
    else:
        form = ProjectSubmissionForm()
    return render(request,"addprojectpage.html",{ 'form' : form })

@login_required
def edit_project_view(request, id_num):
    try:
        objs = Project.objects.get(id=id_num)
    except:
        return HttpResponseRedirect('/')
    if request.user == objs.user:
        form = ProjectSubmissionForm(instance=objs)
        if request.method == 'POST':
            form = ProjectSubmissionForm(request.POST, request.FILES, instance=objs)
            if form.is_valid() and form.has_changed():
                project = form.save(commit=False)
                project.approved = False
                project.save_form()
                schoolAdminGroup = str(form.cleaned_data['school']) + ' Admins'
                relevantUsers = User.objects.filter(Q(groups__name__exact=schoolAdminGroup) | Q(is_superuser=True))
                reversedUrl = ''
                if os.environ.get('DJANGO_ENV') == 'production':
                    reversedUrl = f'https://researchprojectsdemo.azurewebsites.net/admin/hmsSite/project/{project.id}/change/'
                else:
                    reversedUrl = f'http://127.0.0.1:8000/admin/hmsSite/project/{project.id}/change/'
                for user in relevantUsers:
                    user.email_user(
                        f'A new project - {project.title} - has been edited by {project.user.get_full_name()}',
                        f'''Hello {user.get_full_name()},\r\n\r\nA project - {project.title} - has been edited by {project.user.get_full_name()}. 
                        Please review this project at your earliest convenience at {reversedUrl}.\r\n\r\nThis is an automated email. Please do not reply to it.'''
                    )
                project.user.email_user(
                f'Your project - {project.title} - is awaiting approval',
                f' Hello {project.user.get_full_name()},\r\n\r\nYour project has been succesfully edited and is awaiting reapproval by a moderator.\r\n\r\nThis is an automated email. Please do not reply to it.',
                ''
                )
                return HttpResponseRedirect('/')
        return render(request, "addprojectpage.html", { 'form' : form , 'edit' : True})
    else:
        return render(request, "error_403.html", {})

def individual_project_page_view(request, id_num):
    try:
        objs = Project.objects.get(id=id_num)
    except:
        return HttpResponseRedirect('/')
    if objs.approved == True:
        context = {
            "object" : objs,
        }
        return render(request,"individual_project_page.html",context)
    else:
        return HttpResponseRedirect('/')

def eoi_view(request, id_num):
    try:
        objs = Project.objects.get(id=id_num)
    except:
        return HttpResponseRedirect('/')
    if objs.approved == True:
        context = {
            "object" : objs,
        }
        return render(request,"eoi.html",context)
    else:
        return HttpResponseRedirect('/')

@login_required
def still_relevant_view(request, id_num):
    try:
        objs = Project.objects.get(id=id_num)
    except:
        return HttpResponseRedirect('/')
    if objs.approved == True and request.user == objs.user:
        if request.method == 'POST':
            form = StillRelevantForm(request.POST)
            if form.is_valid():
                still_relevant = form.cleaned_data['still_relevant']
                not_relevant = form.cleaned_data['not_relevant']
                edit = form.cleaned_data['edit']
                if still_relevant:
                    objs.last_reminder = date.today
                    objs.email_sent = False
                elif not_relevant:
                    objs.archive()
                elif edit:
                    objs.last_reminder = date.today
                    objs.email_sent = False
                    return HttpResponseRedirect(f'/project/{id_num}/edit/')
            return HttpResponseRedirect(f'/project/{id_num}/')
        else:
            form = StillRelevantForm()
        return render(request,"relevant_page.html",{ 'form' : form })
    else:
        return render(request, "error_403.html", {})

def search_view(request,*args, **kwargs):
    #Filters 
    def title_filter(object):
        if request.GET.get('search_title'):
            get_search_title = request.GET.get('search_title')
            return object.title.lower().find(get_search_title.lower()) > -1
        return True
        
    def desc_filter(object):
        if request.GET.get('desc_title'):
            get_search_desc = request.GET.get('desc_title')
            return object.desc.lower().find(get_search_desc.lower()) > -1
        return True

    def short_desc_filter(object):
        if(request.GET.get('short_desc')):
            get_short_desc = request.GET.get('short_desc')
            return object.short_desc.lower().find(get_short_desc.lower()) > -1
        return True
    
    def qualifications_filter(object):
        if(request.GET.get('qualifications')):
            get_qualifications = request.GET.get('qualifications')
            return object.qualifications.lower().find(get_qualifications.lower()) > -1
        return True

    def contact_name_filter(object):
        if(request.GET.get('contact_name')):
            get_contact_name = request.GET.get('contact_name')
            return (object.contact1_name.lower().find(get_contact_name.lower()) > -1 
                or object.contact2_name.lower().find(get_contact_name.lower()) > -1)
        return True

    def faculty_filter(object):
        if(request.GET.get('faculty')):
            return object.faculty.name == request.GET.get('faculty')
        return True

    def school_filter(object):
        if(request.GET.get('school')):
            return object.school.name == request.GET.get('school')
        return True

    def approved_filter(object):
        return object.approved
    

    '''Sort by'''
    order = request.GET.get('sort_by')
    if(order and order != "default"):
        if order == "title_AtoZ":
            option = Lower("title")
        elif order == "title_ZtoA":
            option = Lower('title').desc()
        elif order == "start_date_newest":
            option = '-start_date'
        elif order == "start_date_oldest":
            option = "start_date" 
        elif order == "end_date_newest":
            option = '-end_date'
        elif order == "end_date_oldest":
            option = "end_date"
    else:
        order = "default"
        option ="-id"

    ''''''
    
    objs = Project.objects.all().order_by(option)

    if request.GET.get('search_simple'):
        simple_kw = request.GET.get('search_simple')

        objs = Project.objects.filter(Q(title__icontains=simple_kw)
            |Q(desc__icontains=simple_kw)| Q(short_desc__icontains=simple_kw)
            |Q(readings__icontains=simple_kw)|Q(goals__icontains=simple_kw)
            |Q(collab__icontains=simple_kw)|Q(funds__icontains=simple_kw)
            |Q(benefits__icontains=simple_kw)|Q(scholarships__icontains=simple_kw)
            |Q(other__icontains=simple_kw)|Q(qualifications__icontains=simple_kw)
            |Q(pref_qualifications__icontains=simple_kw)|Q(contact1_name__icontains=simple_kw)
            |Q(contact1_email__icontains=simple_kw)|Q(contact1_phone__icontains=simple_kw)
            |Q(contact2_name__icontains=simple_kw)|Q(contact2_email__icontains=simple_kw)
            |Q(contact2_phone__icontains=simple_kw)|Q(faculty__name__icontains=simple_kw)
            |Q(school__name__icontains=simple_kw)).order_by(option)

        filterd_objects = filter(approved_filter, objs)

    else:
        filterd_objects = filter(approved_filter,objs)
        filterd_objects = filter(title_filter,filterd_objects)
        filterd_objects = filter(desc_filter,filterd_objects)
        filterd_objects = filter(short_desc_filter,filterd_objects)
        filterd_objects = filter(qualifications_filter,filterd_objects)
        filterd_objects = filter(contact_name_filter,filterd_objects)
        filterd_objects = filter(faculty_filter,filterd_objects)
        filterd_objects = filter(school_filter,filterd_objects)
    

    ''' Paginating '''

    if request.method == "GET":
        paginator = Paginator(list(filterd_objects),10)
        page_num = request.GET.get('page')
    
        try:
            # Get objects on page_num
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # Return the 1st page iff the page num is not integer
            page_obj = paginator.page(1)
        except InvalidPage:
            return HttpResponseNotFound("Error: Page number not found")
        except EmptyPage:
            # Return the last page iff the requested page is out of bound
            page_obj = paginator.page(paginator.num_pages)
    ''''''


    ''' Random 3 projecrts for carousel '''
    objs = Project.objects.all()
    randomlist = random.sample(range(1, len(objs) ), 3)
    randomlist_object_1 = objs.filter(id=randomlist[0])
    randomlist_object_2 = objs.filter(id=randomlist[1])
    randomlist_object_3 = objs.filter(id=randomlist[2])
 
    context = {
            'current_order': order,
            'objects': page_obj,
            'random_object_1' : randomlist_object_1,
            'random_object_2' : randomlist_object_2,
            'random_object_3' : randomlist_object_3,
    }
    return render(request,"search.html",context)

