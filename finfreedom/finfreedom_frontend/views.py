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
from os import stat
import re
from django import http
from django.contrib.auth.models import User
from django.core.checks.messages import DEBUG
from django.db.models import query
from django.db.models.query import QuerySet, prefetch_related_objects
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import requires_csrf_token
from django.views import generic

# from rest_framework.serializers import LIST_SERIALIZER_KWARGS
from .models import *
# from .serializers import *
from django.http import Http404, JsonResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import request, status, viewsets, generics, mixins
from datetime import datetime, timedelta
# from rest_framework.decorators import action, api_view
# from .services import *
from copy import deepcopy
import time
import json
import pytz
import pprint

# Create your views here.
def login(request):
    print("Reached the Login Page")
    print("login request: ", request.method)
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

def overview(request):
    print("reaced the overiew function")
    print("Profile ID: ", request.session['profile_id'])
    profile_object = Profiles.objects.filter(profile_id = request.session['profile_id']).values('profile_id', 'first_name', 'last_name')[0]
    print("Profile Object: ", profile_object)
    context = {
        'profile_name': profile_object['first_name'] + " " + profile_object['last_name'] , 
        'profile_id' : profile_object['profile_id']
    }

    return render(request, 'pages/overview.html', context)

def manage(request):
    print("reaced the manage function")
    print("Profile ID: ", request.session['profile_id'])
    profile_object = Profiles.objects.filter(profile_id = request.session['profile_id']).values('profile_id', 'first_name', 'last_name')[0]
    print("Profile Object: ", profile_object)
    context = {
        'profile_name': profile_object['first_name'] + " " + profile_object['last_name'], 
        'profile_id' : profile_object['profile_id'],
    }
    return render(request, 'pages/manage.html', context)

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

def create_account(request):
    data = json.loads(request.POST['data'])
    profile_info = data['profile_info']
    employer_info = data['employer_info']
    try:
        createSuperUser(
            profile_info['username'], 
            profile_info['password'],
            profile_info['email'],
            profile_info['first_name'],
            profile_info['last_name']
        )

        profile_obj = Profiles.objects.filter(email=profile_info['email'])[0]
        if(profile_obj is None):
            return JsonResponse({"response": "Profile was not created!"})
        employer_object = Employer(
            profile_id=profile_obj, 
            name_of_employer=employer_info['employer_name'], 
            salary=employer_info['salary'],
            position=employer_info['position'],
            income_date=employer_info['income_date'],
            income_frequency=int(employer_info['income_frequency']),
        )
        employer_object.save()
        return JsonResponse({"response": "success", "message": profile_info['username'] + " account has successfully been created!"})
    except Exception as e:
        return JsonResponse({"response":  "Error", "message" : str(e)})

def createSuperUser(username, password, email = "", firstName = "", lastName = ""):
    invalidInputs = ["", None]

    if username.strip() in invalidInputs or password.strip() in invalidInputs:
        return None

    profile_object = Profiles(
        first_name=firstName,
        last_name=lastName,
        email=email,
        username=username,
        password=password,
    )
    profile_object.save()
    user = User(
        username = username,
        email = email,
        first_name = firstName,
        last_name = lastName,
    )
    user.set_password(password)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    return user

def get_company_by_type(request):
    accounts_list_query = ProfileAccountMapping.objects.filter(profile_id=request.POST['profile_id'], account_id__type_of_account=request.POST['type_of_acc']).values_list('account_id')
    accounts_list = []
    if len(accounts_list_query) > 0:
        for acc in accounts_list_query[0]:
            accounts_list.append(acc)
    accounts_companies = Accounts.objects.filter(account_id__in=accounts_list).values()
    results = []
    for acc_info in accounts_companies:
        results.append({
            "value": acc_info['account_id'],
            "text": acc_info['company_name'].capitalize(),
        })
    return JsonResponse({"results": results})

def create_transaction(request):
    data = json.loads(request.POST['data'])
    print(data)
    try:
        transaction_info = data['transaction_info']
        account_object = Accounts.objects.filter(account_id=transaction_info['account_id'])
        transaction_object = Transactions(
            account_id=account_object[0], 
            amount=transaction_info['amount'],
            date_occured=transaction_info['date_occured'],
            name_of_recipient=transaction_info['name_of_recipient'],
        )
        transaction_object.save()
    except Exception as e:
        print("System-Error: ", str(e))
        return JsonResponse({"response": "error", "message": "Failed to Created Transaction!", "system_error": str(e)})
    return JsonResponse({"response": "success", "message": "Successfully Created Transaction!"})