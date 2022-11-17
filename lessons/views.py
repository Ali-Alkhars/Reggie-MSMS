from django.shortcuts import render
from .forms import LessonRequestForm

# Create your views here.
def lesson_request(request):
    if request.method == "POST":
        form = LessonRequestForm(request.POST)
    
    form = LessonRequestForm()
    return render(request, "lesson_request.html", {"form":form})

def lesson_page(request):
    return render(request, "lesson_page.html");

def lesson_admin(request):
    return render(request, "lesson_admin.html");