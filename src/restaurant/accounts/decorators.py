from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

def unauthenticated_user(view_func):        #redirects the user if they are not authorized ot view the page
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):        #decorator that checks the role of the user and the allowed roles to see if the user can view the page
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group =None
            if request.user.groups.count()>0:
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else: 
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


