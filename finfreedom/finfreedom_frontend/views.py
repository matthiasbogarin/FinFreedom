from django.shortcuts import redirect, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *
from datetime import datetime, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.
def login(request):
    print("Reached the Login Page")
    if 'POST' == request.method:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                request.session["profile_id"] = Profiles.objects.filter(email=user.email).values('profile_id').first()["profile_id"]
                response = HttpResponseRedirect('overview')
                auth_login(request, user)
                if 'remember' in request.POST and 'on' == request.POST['remember']:
                    response.set_cookie('FinFreedom_user', request.POST['username'], max_age=None)
                else:
                    response.delete_cookie('FinFreedom_user')
                return response
        else:
            messages.error(request,'username or password not correct')
            response = HttpResponseRedirect('/')
            return response
    if request.COOKIES.get('FinFreedom_user', False):
        return render(request, 'login/login.html', {'username': request.COOKIES.get('FinFreedom_user')})

    return render(request, 'login/login.html')

def logout_view(request):
    print(request)
    auth_logout(request)
    response = HttpResponseRedirect('/')
    return response

def create_account(request):
    print("Create Account request: ", request)
    if 'POST' == request.method:
        print("request Object", request)
    return HttpResponseRedirect("/")

def overview(request):
    print("reaced the overiew function")
    print("Profile ID: ", request.session['profile_id'])
    profile_object = Profiles.objects.filter(profile_id = request.session['profile_id']).values('profile_id', 'first_name', 'last_name')[0]
    print("Profile Object: ", profile_object)
    context = {}

    return render(request, 'pages/overview.html', 
    {
        'profile_name': profile_object['first_name'] + " " + profile_object['last_name'] , 
        'profile_id' : profile_object['profile_id']
    })

def manage(request):
    print("reaced the manage function")
    return render(request, 'pages/manage.html')

def transactions(request):
    print("reaced the transactions function")
    return render(request, 'pages/transactions.html')

def subscriptions(request):
    print("reaced the subscriptions function")
    return render(request, 'pages/subscriptions.html')

def accounts(request):
    print("reaced the accounts function")
    return render(request, 'pages/accounts.html')

def profile(request):
    print("reaced the profile function")
    return render(request, 'pages/profile.html')
