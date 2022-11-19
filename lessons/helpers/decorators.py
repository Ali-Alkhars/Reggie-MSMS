from django.conf import settings
from django.shortcuts import redirect

"""A decorator which doesn't allow users who are logged-in to access a page"""
def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

"""
A decorator used to allow only the users who belong to one of the groups
given in the parameter list to access a page
"""
def permitted_groups(group_names = []):
    def decorator(view_function):
        def wrapper(request):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            # Take user to the page if they are allowed
            if group in group_names:
                return view_function(request)
            # else take them to the default page
            else:
                return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)

        return wrapper
    return decorator
