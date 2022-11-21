from django.shortcuts import render, redirect
from .forms import LessonRequestForm
from .models import Lesson_request
from django.contrib import messages
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request,"home.html")

# Request a lesson using form
# @login_required
# @permitted_groups(['student'])
def lesson_request(request):
    if request.method == "POST":
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submitted successfully")
            availableDays = form.cleaned_data['availableDays']
            availableTimes = form.cleaned_data['availableTimes']
            numberOfLessons = form.cleaned_data['numberOfLessons']
            IntervalBetweenLessons = form.cleaned_data['IntervalBetweenLessons']
            DurationOfLesson = form.cleaned_data['DurationOfLesson']
            LearningObjectives = form.cleaned_data['LearningObjectives']
            AdditionalNotes = form.cleaned_data['AdditionalNotes']
            context = {'availableDays': availableDays, 'availableTimes': availableTimes, 'numberOfLessons': numberOfLessons, 'IntervalBetweenLessons': IntervalBetweenLessons, 'DurationOfLesson': DurationOfLesson, 'LearningObjectives':LearningObjectives, 'AdditionalNotes': AdditionalNotes}
            # render(request, "lesson_page.html", context)
            return redirect("lesson_page")
    else:
        form = LessonRequestForm()
    return render(request, "lesson_request.html", {"form":form})

# @login_required
# @permitted_groups(['student'])
def lesson_page(request):
    data = {'object_list':Lesson_request.objects.all()}
    return render(request, "lesson_page.html", data);

# @login_required
# @permitted_groups(['admin', 'director'])
def lesson_admin(request):
    return render(request, "lesson_admin.html");

    
