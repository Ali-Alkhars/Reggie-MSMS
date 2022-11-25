from django.shortcuts import render, redirect
from django.conf import settings
from lessons.forms import LogInForm, NewLessonForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

"""
The home page that users see when they log in
"""
@login_required
def home(request):
    return render(request, 'home.html', {'home': home})

"""
The main landing page where users can sign-in or register as students
"""
@login_prohibited
def main(request):
    return render(request, 'main.html')

#The majority of these functions need overriding in some way (validation etc)

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

#TODO: Merge with log-in task

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

"""
A page for students to make a lesson request
NOT YET FULLY IMPLEMENTED
"""
@login_required
@permitted_groups(['student'])
def new_lesson(request):

    form = NewLessonForm()
    return render(request, 'new_lesson.html', {'form': form})

"""
A page for admins and directors to check students' lesson requests
NOT YET FULLY IMPLEMENTED
"""
@login_required
@permitted_groups(['admin', 'director'])
def lesson_requests(request):
    return render(request, 'temp.html')

