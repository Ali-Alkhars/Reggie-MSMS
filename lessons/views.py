from django.shortcuts import render, redirect
from .forms import LogInForm, SignUpForm, NewBookingForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'home.html')


def sign_up(request):

    form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def log_in(request):

    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def main(request):
    return render(request, 'main.html', {'main': main})

def new_booking(request):

    form=NewBookingForm()
    return render(request, 'new_booking.html', {'form': form})
