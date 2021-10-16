from django.shortcuts import redirect, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout
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
    logout(request)
    # Redirect to a success page.

def overview(request):
    print("reaced the overiew function")
    return render(request, 'pages/overview.html')
