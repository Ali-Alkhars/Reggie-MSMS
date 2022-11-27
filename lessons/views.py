from django.shortcuts import render, redirect
from .forms import LessonRequestForm
from .models import Lesson_request
from django.contrib import messages
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required
from lessons.helpers.helper_functions import get_user_group


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
            # form_to_be_submitted = form.save(commit=False)
            # form_to_be_submitted.student = request.user
            # form_to_be_submitted.save()
            return redirect("lesson_page")
    else:
        form = LessonRequestForm()
    return render(request, "lesson_request.html", {"form":form})

# @login_required
# @permitted_groups(['student'])
def lesson_page(request):
    # isStudent = userOrAdmin(request);
    # if (isStudent):
        # user_lessons = Lesson_request.objects.filter(student=request.user)
        # data = {'object_list': user_lessons}
    # else:
        # data = {'object_list': Lesson_request.objects.all()}}
    data = {'object_list':Lesson_request.objects.all()}
    return render(request, "lesson_page.html", data);

# @login_required
# @permitted_groups(['admin', 'director'])
def lesson_admin(request):
    user_lessons = Lesson_request.objects.filter(user=request.user)
    data = {'object_list':user_lessons}
    return render(request, "lesson_admin.html", data);

def userOrAdmin(request):
    if (get_user_group(request) == 'student'):
        return True
    return False


    
