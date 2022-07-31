from tokenize import group
from django import views
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('working:', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Restriced content")
        return wrapper_func
    return decorator


def managers_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'members':
                return redirect('tasks')
            if group == 'registered':
                return redirect('profile-settings')
            if group == 'managers':
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not our member")
    return wrapper_func
        
           