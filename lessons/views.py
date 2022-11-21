from django.shortcuts import render
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required

"""
Home page for all users.
TEMPORARILY ADDED FOR TESTING
"""
def home(request):
    return render(request, 'temp.html')

"""
A page for students to register an account
"""
@login_prohibited
def register(request):
    return render(request, 'temp.html')

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
