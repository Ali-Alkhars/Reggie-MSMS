from django.shortcuts import render, redirect
from .forms import LogInForm, SignUpForm, NewBookingForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'home.html', {'home': home})

def main(request):
    return render(request, 'main.html')

#The majority of these functions need overriding in some way (validation etc)

#TODO: Merge with sign_up form
def sign_up(request):
    form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

#TODO: Merge with log-in task
def log_in(request):

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

#Temporary placeholder for new booking form (this one is currently empty)
def new_booking(request):

    form=NewBookingForm()
    return render(request, 'new_booking.html', {'form': form})
