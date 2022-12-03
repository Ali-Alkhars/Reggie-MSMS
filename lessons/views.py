import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from lessons.forms import LogInForm, RegisterForm, EditLoginsForm, EditPasswordForm, LessonRequestForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required
from lessons.models import User, LessonRequest
from lessons.helpers.helper_functions import promote_admin_to_director, delete_user, get_user_full_name
from django.contrib import messages
import  logging
logger = logging.getLogger(__name__)

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


# The majority of these functions need overriding in some way (validation etc)

"""
A page for students to register an account
"""


@login_prohibited
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save_user_as_student()
            login(request, user)
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        form = RegisterForm()
    return render(request, 'register_as_student.html', {'form': form, 'submitText': 'Register'})


"""
A view for users to log-in
"""


@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
                return redirect(redirect_url)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    else:
        next = request.GET.get('next') or ''
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'next': next, 'submitText': 'Login'})


"""
A view to make users log-out
"""


def log_out(request):
    logout(request)
    return redirect('main')


@login_required
def bookings(request):
    return render(request, 'bookings.html')


# ****************************** Lesson Request ****************************** #

"""
A page for students to make a lesson request
NOT YET FULLY IMPLEMENTED
"""


@login_required
@permitted_groups(['student'])
def new_lesson(request):
    context = {}
    form = LessonRequestForm(request.POST or None)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('lesson_requests')
    context['form'] = form
    context["title"] = "New Lesson Request"
    return render(request, 'new_lesson.html', context)


"""
A page for admins and directors to check students' lesson requests
NOT YET FULLY IMPLEMENTED
"""


@login_required
@permitted_groups(['admin', 'director'])
def lesson_requests(request):
    context = {}
    if request.user.groups.filter(name='admin').exists():
        context["dataset"] = LessonRequest.objects.all()
        context["type"] = "admin"
    elif request.user.groups.filter(name='student').exists():
        context["dataset"] = LessonRequest.objects.filter(user=request.user)
        context["type"] = "student"
    return render(request, 'lesson_requests.html', context)


@login_required
def lesson_requests_list(request):
    context = {}
    if request.user.groups.filter(name='admin').exists():
        return lesson_requests(request)
    elif request.user.groups.filter(name='student').exists():
        context["dataset"] = LessonRequest.objects.filter(user=request.user)
        context["type"] = "student"
    return render(request, 'lesson_requests.html', context)

@login_required
@permitted_groups(['admin', 'student'])
def lesson_requests_edit(request, lesson_request_id):
    context = {}
    obj = get_object_or_404(LessonRequest, id=lesson_request_id)
    form = LessonRequestForm(request.POST or None, instance=obj)

    if(obj.booked):
        return HttpResponseRedirect('/lesson_requests')

    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/lesson_requests')

    context["form"] = form
    context["title"] = "Edit Lesson Request"
    return render(request, 'new_lesson.html', context)

@login_required
@permitted_groups(['admin', 'student'])
def lesson_requests_delete(request, lesson_request_id):
    context = {}
    obj = get_object_or_404(LessonRequest, id=lesson_request_id)
    obj.delete()
    return HttpResponseRedirect('/lesson_requests')


@login_required
@permitted_groups(['admin', 'student'])
def lesson_requests_details(request, lesson_request_id):
    context = {'data': get_object_or_404(LessonRequest, id=lesson_request_id)}
    return render(request, 'lesson_request_details.html', context)


# ****************************** End of Lesson Request ****************************** #


"""
A page for directors to view/edit/delete admin accounts or promote
them to directors
"""


@login_required
@permitted_groups(['director'])
def admin_accounts(request):
    if request.method == 'POST':
        user_type = request.POST.get("user_type")
        return redirect('register_super', user_type)

    admins = User.objects.filter(groups__name='admin')
    return render(request, 'admin_accounts.html', {'admins': admins})


"""
A view which does the page redirections for the action buttons
in the admin_accounts view
"""


@login_required
@permitted_groups(['director'])
def admin_actions(request, action, user_id):
    if action == 'promote':
        promote_admin_to_director(user_id)
        messages.add_message(request, messages.SUCCESS,
                             f"{get_user_full_name(user_id)} has been successfully promoted to a director!")

    elif action == 'edit':
        return redirect('edit_admin', 'None', user_id)

    elif action == 'delete':
        messages.add_message(request, messages.SUCCESS, f"{get_user_full_name(user_id)} has been successfully deleted!")
        delete_user(user_id)

    return redirect('admin_accounts')


"""
A view for directors to edit the account of an admin
"""


@login_required
@permitted_groups(['director'])
def edit_admin(request, action, user_id):
    admin_user = User.objects.get(id=user_id)
    edit_logins_form = EditLoginsForm(instance=admin_user)
    edit_password_form = EditPasswordForm()

    if request.method == 'POST':
        # User chose to update the admin's login info
        if action == 'logins':
            edit_logins_form = EditLoginsForm(instance=admin_user, data=request.POST)
            if edit_logins_form.is_valid():
                messages.add_message(request, messages.SUCCESS, "Admin login information updated!")
                edit_logins_form.save()
                return redirect('edit_admin', 'None', user_id)

        # User chose to update the admin's password
        elif action == 'password':
            edit_password_form = EditPasswordForm(data=request.POST)
            if edit_password_form.is_valid():
                current_password = edit_password_form.cleaned_data.get('current_password')
                if check_password(current_password, admin_user.password):
                    new_password = edit_password_form.cleaned_data.get('new_password')
                    admin_user.set_password(new_password)
                    admin_user.save()
                    messages.add_message(request, messages.SUCCESS, "Admin password updated!")
                    return redirect('edit_admin', 'None', user_id)

        # User is done editing
        else:
            return redirect('admin_accounts')

    return render(request, 'edit_admin.html',
                  {'logins_form': edit_logins_form, 'password_form': edit_password_form, 'user_id': user_id})


"""
A page for directors to create either an admin or director account
"""


@login_required
@permitted_groups(['director'])
def register_super(request, user_type):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if user_type == 'director':
                form.save_user_as_director()
            else:
                form.save_user_as_admin()

            return redirect('admin_accounts')
    else:
        form = RegisterForm()

    if user_type == 'director':
        return render(request, 'register_as_director.html', {'form': form})
    else:
        return render(request, 'register_as_admin.html', {'form': form})
