from genericpath import exists
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, managers_only
from django.core.mail import EmailMessage
from core import settings
from django.template.loader import render_to_string

import os



# Create your views here.
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        member = authenticate(request, username=username,password=password)
        if member is not None:
            login(request,member)
            return redirect('dashboard')
    context = {}
    return render(request, 'cms/login.html', context)

@unauthenticated_user
def loginFirstPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        member = authenticate(request, username=username,password=password)
        if member is not None:
            login(request,member)
            return redirect('profile-settings')
    context = {}
    return render(request, 'cms/login-first.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

#login_required(login_url='login')
#@managers_only
def registerPage(request):
    form = CreateMemberForm()
    if request.method == "POST":
        form = CreateMemberForm(request.POST)
        user = form.save()
        group = Group.objects.get(name='registered')
        user.groups.add(group)
        return redirect('login')
    context = {'form':form}
    return render(request, 'cms/register.html', context)



@login_required(login_url='login')
@managers_only
def dashboard(request):
    tasks = Task.objects.all().order_by('due_date', 'due_time')
    task_count = Task.objects.all().count()
    uncompleted_task_task_count = Task.objects.filter(complete = False).count()
    if task_count == 0:
        value = (uncompleted_task_task_count * 100)/1
        x = 0
        y = 0
    else:
        value = (uncompleted_task_task_count * 100)/task_count
        formatted_value = "{:.2f}".format(value)
        x=float(formatted_value)
        y = 100-x
    
    #Notification count
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    requests = MemberRequest.objects.filter(to_user=request.user, is_resolved=False)
    requests_notification = requests.count()
    context = {'tasks': tasks, 'task_count': task_count, 'x': x, 'y': y,'requests': requests, 'tasks_notification':tasks_notification, 'requests_notification': requests_notification}
    print(task_count)
    return render(request, 'cms/dashboard.html', context)




@login_required(login_url='login')
def tasks(request):
    tasks = Task.objects.filter(member=request.user).order_by('due_date', 'due_time')
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    requests = MemberRequest.objects.filter(to_user=request.user, is_resolved=False)
    requests_notification = requests.count
    context = {'tasks': tasks, 'tasks_notification': tasks_notification, 'requests': requests, 'requests_notification': requests_notification}
    return render(request, 'cms/tasks.html', context)


@login_required(login_url='login')
def tasksCompleted(request):
    tasks = Task.objects.filter(member=request.user, complete = True)
    tasks_count = tasks.filter(complete = False ).count()

    #Notification count
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    requests = MemberRequest.objects.all()
    requests_notification = requests.count
    context = {'tasks': tasks, 'tasks_notification': tasks_notification, 'requests':requests, 'requests_notification': requests_notification}
    return render(request, 'cms/tasks-completed.html', context)


@login_required(login_url='login')
def tasksDue(request):
    tasks = Task.objects.filter(member=request.user, complete = False)

    #Notification count
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    context = {'tasks': tasks, 'tasks_notification': tasks_notification}
    return render(request, 'cms/tasks-due.html', context)


@login_required(login_url='login')
def addTask(request):
    form = AddTaskForm()
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()

    context = {'form':form, 'tasks_notification': tasks_notification}
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            submited_task = form.save(commit=False)
            submited_task.author = request.user
            form.save()
            member_assigned = form.cleaned_data['member']
            title = form.cleaned_data['title']
            due_date = form.cleaned_data['due_date']
            due_time = form.cleaned_data['due_time']
            context = {'title': title, 'due_date': due_date, 'due_time': due_time}
            email_template = render_to_string('cms/emails/task.html', context)

            email = EmailMessage(
                'New task assigned to you',
                email_template,
                settings.EMAIL_HOST_USER,
                [member_assigned.email]
            )
            email.fail_silently = False
            try:
                email.send()
            except:
                return HttpResponse("Task added but notification has not been sent.")
            return redirect('tasks')
    return render(request, 'cms/add-task.html', context)

@login_required(login_url='login')
def editTask(request, pk):
    task = Task.objects.get(id=pk)
    form = AddTaskForm(instance=task)
    if request.method == 'POST':
        form = AddTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'cms/edit-task.html', context)

@login_required(login_url='login')
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)

    #Notification count
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    context = {'task': task, 'tasks_notification': tasks_notification}
    return render(request, 'cms/task.html', context)


@login_required(login_url='login')
def completeTask(request,pk):
   task = Task.objects.get(id=pk)
   task.complete = True
   task.save()
   title = task.title
   member = task.member.email
   author = task.author.email
   print(author)
   context = {'title': title, 'member': member}
   email_template = render_to_string('cms/emails/task_complete.html', context)
   email = EmailMessage(
       'Task completed',
       email_template,
       settings.EMAIL_HOST_USER,
       [author]
   )
   email.fail_silently = False
   email.send()
   return redirect('dashboard')


@login_required(login_url='login')
def deleteTask(request,pk):
   task = Task.objects.get(id=pk)
   task.delete()
   return redirect('dashboard')

@login_required(login_url='login')
def activities(request):
    activities = Activity.objects.all()

    #Notification count
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    context = {'activities': activities, 'tasks_notification' :tasks_notification}
    return render(request, 'cms/activities.html', context)


@login_required(login_url='login')
def addActivity(request):
    form = AddActivityForm()
    context = {'form':form}
    if request.method == 'POST':
        form = AddActivityForm(request.POST)
        if form.is_valid():
            user_request = form.save(commit=False)
            user_request.author = request.user
            form.save()
            return redirect('activities')
        else:
            form = AddActivityForm()
    return render(request, 'cms/add-activity.html', context)


@login_required(login_url='login')
def completeActivity(request, pk):
    activity = Activity.objects.get(id=pk)
    activity.complete = True
    activity.save()
    return redirect('activities')

@login_required(login_url='login')
def deleteActivity(request, pk):
    activity = Activity.objects.get(id=pk)
    activity.delete()
    return redirect('activities')


@login_required(login_url='login')
@managers_only
def members(request):
    members_list = User.objects.all()
    context = {'members_list': members_list}
    return render(request, 'cms/members.html', context)

def approveMember(request, pk):
    user = Member.objects.get(id=pk)
    group = Group.objects.get(name='members')
    user.groups.add(group)
    return render ('member-profile.html')

@login_required(login_url='login')
def addmember(request):
    form = AddMemberForm()
    print(member)
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            if member.exists():
                return HttpResponse("Profile already exits")
            form.save()
            return redirect('members')
    context = {'form': form}
    return render(request, 'cms/add-member.html', context)


@login_required(login_url='login')
@managers_only
def editmember(request, pk):
    member = member.objects.get(id=pk)
    form = MemberForm(instance=member)
    context = {'form': form}
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members')
    return render(request, 'cms/edit-member.html', context)
    

@login_required(login_url='login')
def member(request, pk):
    member  = User.objects.get(id = pk)
    profile = Member.objects.filter(username = pk)
    context = {"member": member, 'profile': profile}
    return render(request, 'cms/member.html', context)

@login_required(login_url='login')
def profile(request):
    member  = Member.objects.get(username = request.user)
    context = {"member": member}
    return render(request, 'cms/profile.html', context)

@login_required(login_url='login')
def profileSettings(request):
    form = MemberForm()
    member = Member.objects.filter(username = request.user)
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            current_user.username = request.user
            if member.exists():
                return HttpResponse("Profile already exists")
            form.save()
            group = Group.objects.get(name='members')
            current_user = request.user
            current_user.groups.add(group)
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'cms/profile-settings.html', context)



@login_required(login_url='login')
def userRequest(request, pk):
    userrequest = MemberRequest.objects.get(id=pk)
    context = {'userrequest': userrequest}
    return render(request, 'cms/user-request.html', context)


@login_required(login_url='login')
def userRequests(request):
    requests = MemberRequest.objects.filter(to_user=request.user).order_by('-requested_at')
    unresolved_requests = MemberRequest.objects.filter(to_user=request.user, is_resolved=False)
    requests_notification = unresolved_requests.count
    tasks_notification = Task.objects.filter(member=request.user, complete = False).count()
    context = {'tasks': tasks, 'tasks_notification': tasks_notification, 'requests': requests, 'requests_notification': requests_notification}
    return render(request, 'cms/user-requests.html', context)


@login_required(login_url='login')
def submitRequest(request):
    form = SubmitRequest()
    if request.method == 'POST':
        form = SubmitRequest(request.POST)
        if form.is_valid():
            submited_request = form.save(commit=False)
            submited_request.from_user = request.user
            submited_request.is_resolved = False
            form.save()
            form_user = request.user.first_name
            to_user = form.cleaned_data['to_user']
            title = form.cleaned_data['title']
            to_user_name = to_user.first_name
            context = {'to_user_name': to_user_name, 'form_user': form_user, 'title': title}
            email_template = render_to_string('cms/emails/request.html', context)

            email = EmailMessage(
                'New requst is sent to you!',
                email_template,
                settings.EMAIL_HOST_USER,
                [to_user.email],
            )
            email.fail_silently = False
            email.send()
            return redirect('dashboard')
        else:
            form = SubmitRequest()
    context = {'form':form}
    return render(request, 'cms/submi-request.html', context)



@login_required(login_url='login')
def resolveRequest(request, pk):
    userrequest = MemberRequest.objects.get(id=pk)
    userrequest.is_resolved = True
    userrequest.save()
    return redirect ('user-requests')


@login_required(login_url='login')
def deleteRequest(request, pk):
    userrequest = MemberRequest.objects.get(id=pk)
    current_user = request.user
    if userrequest.from_user == current_user:
        userrequest.delete()
    else:
        return HttpResponse("You re not authorised to perfrom that action")
    return redirect ('user-requests')


@login_required(login_url='login')
def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'cms/projects.html', context)

@login_required(login_url='login')
def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project': project}
    return render(request, 'cms/project.html', context)


@login_required(login_url='login')
@managers_only
def addProject(request):
    form = addProjectForm()
    context = {'form': form}
    if request.method == 'POST':
        form = addProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'cms/add-project.html', context)


@login_required(login_url='login')
@managers_only
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    project.delete()
    return redirect('projects')


@login_required(login_url='login')
@managers_only
def completeProject(request, pk):
    project = Project.objects.get(id=pk)
    project.status = 'Complete'
    project.save()
    return redirect('projects')


@login_required(login_url='login')
@managers_only
def uncompleteProject(request, pk):
    project = Project.objects.get(id=pk)
    project.status = 'Uncomplete'
    project.save()
    return redirect('projects')


@login_required(login_url='login')
@managers_only
def editProject(request, pk):
    project = Project.objects.get(id=pk)
    form = addProjectForm(instance=project)
    context = {'form': form}
    if request.method == 'POST':
        form = addProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'cms/edit-project.html', context)




    