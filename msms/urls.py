"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('register/', views.register, name='register'),
    path('register_super/<user_type>', views.register_super, name='register_super'),
    path('new_lesson/', views.new_lesson, name='new_lesson'),
    path('lesson_requests/', views.lesson_requests, name='lesson_requests'),
    path('bookings/', views.bookings, name='bookings'),
    path('admin_accounts/', views.admin_accounts, name='admin_accounts'),
    path('admin_actions/<action>/<int:user_id>', views.admin_actions, name='admin_actions'),
    path('edit_admin/<action>/<int:user_id>', views.edit_admin, name='edit_admin'),
    path('student_invoices/', views.student_invoices, name='student_invoices'),
    path('pay_invoice/<reference>', views.pay_invoice, name='pay_invoice'),
]
