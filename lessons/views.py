from django.conf import settings
from django.shortcuts import render, redirect
from lessons.forms import RegisterForm
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

"""
Home page for all users.
TEMPORARILY ADDED FOR TESTING
"""
def home(request):
    return render(request, 'base.html')

"""
A page for students to register an account
"""
@login_prohibited
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

"""
A page for students to make a lesson request
NOT YET FULLY IMPLEMENTED
"""
@login_required
@permitted_groups(['student'])
def new_lesson(request):
    return render(request, 'temp.html')

"""
A page for admins and directors to check students' lesson requests
NOT YET FULLY IMPLEMENTED
"""
@login_required
@permitted_groups(['admin', 'director'])
def lesson_requests(request):
    return render(request, 'temp.html')
