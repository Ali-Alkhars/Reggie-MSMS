from django.shortcuts import render, redirect
from django.conf import settings
from lessons.forms import LogInForm, NewLessonForm, RegisterForm, EditLoginsForm, EditPasswordForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required
from lessons.models import User
from lessons.helpers.helper_functions import promote_admin_to_director, delete_user, get_user_full_name
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
            user = form.save_user_as_student()
            login(request, user)
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    else:
        form = RegisterForm()
    return render(request, 'register_as_student.html', {'form': form})

#TODO: Merge with log-in task
def log_in(request):

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form, 'post_url' : 'register'})

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
        messages.add_message(request, messages.SUCCESS, f"{get_user_full_name(user_id)} has been successfully promoted to an admin!")
    
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
        
    return render(request, 'edit_admin.html', {'logins_form': edit_logins_form, 'password_form': edit_password_form, 'user_id': user_id})

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

