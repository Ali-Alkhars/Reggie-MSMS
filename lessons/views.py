from django.shortcuts import render, redirect
from django.conf import settings
from .forms import LessonRequestForm, LogInForm, NewLessonForm, RegisterForm, EditLoginsForm, EditPasswordForm
from .models import Lesson_request, User
from django.contrib import messages
from lessons.helpers.decorators import login_prohibited, permitted_groups
from django.contrib.auth.decorators import login_required
from lessons.helpers.helper_functions import get_user_group, promote_admin_to_director, delete_user, get_user_full_name, userOrAdmin
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login, logout

# Request a lesson using form
@login_required
@permitted_groups(['student'])
def lesson_request(request):
    if request.method == "POST":
        form = LessonRequestForm(request.POST)
        if (userOrAdmin(request)):
            field = form.fields['Fulfilled']
            field.widget = field.hidden_widget()
            form.fields['Fulfilled'].disabled = True
        if form.is_valid():
            form_to_be_submitted = form.save(commit=False)
            form_to_be_submitted.student = request.user
            form_to_be_submitted.save()
            return redirect("lesson_page")
    else:
        form = LessonRequestForm()
    return render(request, "lesson_request.html", {"form":form})

@login_required
@permitted_groups(['student', 'admin', 'director'])
def lesson_page(request):
    isStudent = userOrAdmin(request)
    if (isStudent):
        user_lessons = Lesson_request.objects.filter(student=request.user)
        count = Lesson_request.objects.filter(student=request.user).count()
        request.session['countOfTable'] = count
        data = {'object_list': user_lessons, 'count': count, 'currentUser': isStudent}
    else:
        count = Lesson_request.objects.all().count()
        request.session['countOfTable'] = count
        data = {'object_list': Lesson_request.objects.all(), 'count': count, 'currentUser': isStudent}
    return render(request, "lesson_page.html", data)

@login_required
@permitted_groups(['student', 'admin', 'director'])
def lesson_request_update(request, id):
    # if (lesson_request.Fulfilled == 'Denied' | lesson_request.Fulfilled == 'Approved'):
    #     return redirect('lesson_page')
    lesson_request = Lesson_request.objects.get(id=id)
    if request.method == 'POST':
        form = LessonRequestForm(request.POST, instance=lesson_request)
        if (userOrAdmin(request)):
            field = form.fields['Fulfilled']
            field.widget = field.hidden_widget()
            form.fields['Fulfilled'].disabled = True
        if form.is_valid():
            form.save()
            return redirect('lesson_page')
    else:
        form = LessonRequestForm(instance=lesson_request)
    return render(request, 'lesson_request_update.html', {"form": form})

@login_required
@permitted_groups(['student', 'admin', 'director'])
def lesson_request_delete(request, id):
    lesson_request = Lesson_request.objects.get(id=id)

    if request.method == 'POST':
        lesson_request.delete()

        return redirect('lesson_page')
    return render(request, 'lesson_request_delete.html', {'lesson_request': lesson_request})



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
    return render(request, 'log_in.html', {'form': form, 'next': next})

"""
A view to make users log-out
"""
def log_out(request):
    logout(request)
    return redirect('main')

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
        messages.add_message(request, messages.SUCCESS, f"{get_user_full_name(user_id)} has been successfully promoted to a director!")
    
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

