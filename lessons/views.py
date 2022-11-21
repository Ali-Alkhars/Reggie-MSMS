from django.shortcuts import render, redirect
from .forms import LessonRequestForm
from .models import Lesson_request
from django.contrib import messages


# Create your views here.
def home(request):

    return render(request, "home.html")

def lesson_request(request):
    if request.method == "POST":
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submitted successfully")
            return redirect("lesson_page")
    else:
        form = LessonRequestForm()
    return render(request, "lesson_request.html", {"form":form})

def lesson_page(request):
    return render(request, "lesson_page.html");

def lesson_admin(request):
    return render(request, "lesson_admin.html");