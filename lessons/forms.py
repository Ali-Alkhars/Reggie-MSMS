"""Forms for the MSMS app"""
from django import forms
from django.core.validators import RegexValidator
from lessons.models import User, Lesson_request, TermTime
from django.contrib.auth.models import Group
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import datetime


# Request form for the lesson
class LessonRequestForm(forms.ModelForm):
    class Meta:
        model = Lesson_request
        fields = ["availableDays", "availableTimes", "numberOfLessons", "IntervalBetweenLessons", "DurationOfLesson", "LearningObjectives", "AdditionalNotes"]
        labels = {
            'availableDays': "Choose a day: ",
            'availableTimes': "Choose a time: ",
            'numberOfLessons': "Number of lessons desired: ",
            'IntervalBetweenLessons': "Interval between lessons (In weeks): ",
            'DurationOfLesson': "Duration of lesson (In minutes): ",
            'LearningObjectives': "What do you want to learn? ",
            'AdditionalNotes': "Additional notes/comments: " 
        }
        widget = {
            "LearningObjectives": forms.Textarea(),
            "AdditionalNotes": forms.Textarea()
        }

class NewTermForm(forms.ModelForm):
    """Form enabling admins and directors to register term time"""
    startDate = forms.DateField(input_formats = settings.DATE_INPUT_FORMATS, label='Please follow format: yyyy-mm-dd')
    endDate = forms.DateField(input_formats = settings.DATE_INPUT_FORMATS, label='Please follow format: yyyy-mm-dd')
    class Meta:
        model = TermTime
        fields = ["termOrder"]   
        if (TermTime.objects.all().count() == 2):
            widgets = {'termOrder': forms.HiddenInput(),}
    
    def clean(self):
        super().clean()
        startdate = self.cleaned_data.get('startDate')
        enddate = self.cleaned_data.get('endDate')
        termOrderUsed = self.cleaned_data.get("termOrder")
        
        if (startdate is not None and enddate is not None): 
            if enddate <= startdate:
                raise forms.ValidationError("End date should be greater than start date")     
            if abs((enddate - startdate).days) < 90:
                self.add_error('endDate', 'The term should be at least 90 days long.')
    
        if (startdate is not None and enddate is not None):
            if (TermTime.objects.all().count() != 0):
                if (termOrderUsed == "First term"):
                    try:
                        object = TermTime.objects.get(termOrder="Second term")
                        if (object.startDate < enddate):
                            self.add_error('endDate', 'The term must not overlap')
                    except ObjectDoesNotExist:
                        pass   
                else:
                    try: 
                        object = TermTime.objects.get(termOrder="First term")
                        if (object.endDate > startdate):
                            self.add_error('startDate', 'The term must not overlap')
                    except ObjectDoesNotExist:
                        pass

        if (TermTime.objects.filter(termOrder=termOrderUsed).count() != 0):
            if (TermTime.objects.all().count() < 2):
                raise forms.ValidationError("There should only be one term1 and one term2")
        

# This is just a placeholder form
class LogInForm(forms.Form):
    username = forms.EmailField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

# This is just a placeholder form
class NewLessonForm(forms.Form):
    test = forms.CharField(label="TEST")

class RegisterForm(forms.ModelForm):
    """Form enabling students to register an account"""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username']

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            self.add_error('confirm_password', 'Confirmation does not match password.')

    """Assign a given user to the student group"""
    def save_user_as_student(self):
        user = self.save()
        student_group = Group.objects.get(name='student') 
        student_group.user_set.add(user)
        return user
    
    """Assign a given user to the director group"""
    def save_user_as_director(self):
        user = self.save()
        director_group = Group.objects.get(name='director') 
        director_group.user_set.add(user)
        return user
    
    """Assign a given user to the admin group"""
    def save_user_as_admin(self):
        user = self.save()
        admin_group = Group.objects.get(name='admin') 
        admin_group.user_set.add(user)
        return user

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('new_password'),
        )

        return user
    
class EditLoginsForm(forms.ModelForm):
    """Form for users to update their login information"""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username']

class EditPasswordForm(forms.Form):
    """Form for users to update their password"""

    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            self.add_error('confirm_password', 'Confirmation does not match password.')
