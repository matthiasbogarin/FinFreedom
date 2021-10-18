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
from datetime import datetime, timedelta,date
# from rest_framework.decorators import action, api_view
# from .services import *
from copy import deepcopy
import time
import json
import pytz
import pprint
from django.views.generic.base import TemplateView

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
                response = HttpResponseRedirect('accounts')
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
        "page": "Overview",
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
        "page": "Manage",
        'profile_name': profile_object['first_name'] + " " + profile_object['last_name'], 
        'profile_id' : profile_object['profile_id'],
    }
    return render(request, 'pages/manage.html', context)

class accounts(TemplateView):
    template_name = 'pages/accounts.html'
    
    def get(self, request):
        print("reaced the accounts function")
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        profile_object = Profiles.objects.filter(profile_id = request.session['profile_id']).values('profile_id', 'first_name', 'last_name')[0]
        
        #headers
        headers = {'headers':['Type Of Account', 'Company', 'Account Name', "Expiration Date", "Amount on Card", "Credit On Card", "Payment Date"]}
        rows = []
        #get_data using profile_id
        accounts_from_profile = ProfileAccountMapping.objects.all()
        print(accounts_from_profile)
        data = []
        if len(accounts_from_profile) > 0:
            for acct in accounts_from_profile:
                print(acct.profile_id.profile_id)
                if acct.profile_id.profile_id == profile_object['profile_id']:
                    data.append(acct.account_id.account_id)
        print(data)
        account_obj_list = Accounts.objects.filter(account_id__in=data).values()
        if len(account_obj_list) > 0:
            for d in account_obj_list:
                print(d)
                if d['amount_on_card'] == None:
                    amount_on_card = None
                else:
                    amount_on_card = "$" + str(d['amount_on_card'])

                if d['credit_on_card'] == None:
                    credit_on_card = None
                else:
                    credit_on_card = "$" + str(d['credit_on_card'])

                if d['payment_date'] == None:
                    payment_date = None
                else:
                    payment_date = str(currentMonth) + "-" + d['payment_date'] + "-" + str(currentYear)
    
                data = {
                    'account_id': d['account_id'],
                    'type_of_account': d['type_of_account'],
                    'company': d['company_name'], 
                    'account_name': d['account_name'],
                    'expiration_date': d['expiration_date'],
                    'amount_on_card' : amount_on_card,
                    'credit_on_card': credit_on_card,
                    'payment_date': payment_date,
                }
                rows.append(data)

        context = {
            "headers": headers['headers'],
            "rows": rows,
            "page": "Account",
            'profile_name': profile_object['first_name'] + " " + profile_object['last_name'] , 
            'profile_id' : profile_object['profile_id']
        }
        print(context)

        return render(request,self.template_name, context)

class transactions(TemplateView):
    template_name = 'pages/transactions.html'
    
    def get(self, request):
        print("reaced the transactions function")
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        profile_object = Profiles.objects.filter(profile_id = request.session['profile_id']).values('profile_id', 'first_name', 'last_name')[0]
        
        #headers
        headers = {'headers':['Account Name', 'Recipient', 'Amount', "Date"]}
        rows = []
        #get_data using profile_id
        accounts_from_profile = ProfileAccountMapping.objects.all()
        print(accounts_from_profile)
        data = []
        if len(accounts_from_profile) > 0:
            for acct in accounts_from_profile:
                print(acct.profile_id.profile_id)
                if acct.profile_id.profile_id == profile_object['profile_id']:
                    data.append(acct.account_id.account_id)
        print(data)
        transactions_obj_list = Transactions.objects.filter(account_id__account_id__in=data).values()
        print("transactions: ", transactions_obj_list)
        account_obj_list = Accounts.objects.filter(account_id__in=data).values()
        if len(transactions_obj_list) > 0:
            for d in transactions_obj_list:
                print(d)
                print(d['account_id_id'])
                account_obj = Accounts.objects.filter(account_id=d['account_id_id'])[0]
                print(account_obj)
                data = {
                    'transaction_id': d['transaction_id'],
                    'account_name': account_obj.account_name,
                    'recipient': d['name_of_recipient'],
                    'amount': d['amount'], 
                    'date_occured': d['date_occured'],
                }
                rows.append(data)

        context = {
            "headers": headers['headers'],
            "rows": rows,
            "page": "Transaction",
            'profile_name': profile_object['first_name'] + " " + profile_object['last_name'] , 
            'profile_id' : profile_object['profile_id']
        }
        print(context)

        return render(request,self.template_name, context)

def subscriptions(request):
    print("reaced the subscriptions function")
    return render(request, 'pages/subscriptions.html')

def profile(request):
    print("reaced the profile function")
    profile_object = Profiles.objects.filter(profile_id=request.session['profile_id']).values('profile_id', 'first_name', 'last_name', 'username')[0]
    employer_object = Employer.objects.filter(profile_id=profile_object['profile_id']).values('name_of_employer', 'position', 'salary')[0]
    print("Profile Object: ", profile_object)
    print("Employer Object: ", employer_object)

    context = {
        "page": "Profile",
        'profile_name': profile_object['first_name'] + " " + profile_object['last_name'], 
        'profile_id' : profile_object['profile_id'],
        'first_name': profile_object['first_name'],
        'last_name': profile_object['last_name'],
        'username': profile_object['username'],
        'name_of_employer': employer_object['name_of_employer'],
        'position': employer_object['position'],
        'salary': "$" + str(employer_object['salary']),
    }
    return render(request, 'pages/profile.html', context)
 
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

def submit_new_account(request):
    data = json.loads(request.POST['data'])
    print(data)
    account_info = data['account_info']
    profile_id = account_info['profile_id']
    try:
        profile_obj = Profiles.objects.filter(profile_id=profile_id)[0]
        if account_info['credit_on_card'] == '':
            account_info['credit_on_card'] = None
        if account_info['amount_on_card'] == '':
            account_info['amount_on_card'] = None
        new_acc_obj = Accounts(
            type_of_account=account_info['type_of_account'],
            company_name= account_info['company_name'],
            account_name= account_info['account_name'],
            name_on_card=account_info['card_on_name'],
            card_number=account_info['card_number'],
            expiration_date= account_info['expiration_date'],
            security_code= account_info['security_code'],
            payment_date= account_info['payment_day'],
            amount_on_card=account_info['amount_on_card'],
            credit_on_card=account_info['credit_on_card'],
        )
        print(new_acc_obj)
        new_acc_obj.save()
        
        account_obj = Accounts.objects.filter(account_id=new_acc_obj.account_id)[0]
        profileAccountMapObj = ProfileAccountMapping(
            account_id=account_obj,
            profile_id=profile_obj,
            date_connect=date.today()
        )
        profileAccountMapObj.save()
        return JsonResponse({"response":  "success", "message" : "Successfully Created Account!"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"response":  "Error", "message" : str(e)})

def delete_account(request):
    data = json.loads(request.POST['data'])
    try:
        profile_obj = Profiles.objects.filter(profile_id=data['profile_id'])[0]
        account_obj = Accounts.objects.filter(account_id=data['account_id'])[0]
        ProfileAccountMapping.objects.filter(account_id=account_obj, profile_id=profile_obj)[0].delete()
        account_obj.delete()
        return JsonResponse({"response": "success", "message": "Successfully Deleted Account!"})
    except Exception as e:
        print(str(e))
        return JsonResponse({"response": "error", "message": "Failed to delete account!", "system_error": str(e)}) 

# Add a Expense Transaction Function
# This will make a negative Transaction 
# and will be minus from the debit or cash account for the logged in user.
def create_expense_transaction(request):
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


# Add an Income transaction function
# This should create a postive transaction that then is added on to the debit or cash account for the logged in user.
def create_income_transaction(request):
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


# Pay Credit Card function
# This should choose a credit card account to make a transaction for a payment 
# and minus that quantity from the credit card balance of the logged in user.
def pay_credit_transaction(request):
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


# Transfer to saving function
# This should pick a An Account to move the money from to the logged in users savings account.
def transfer_to_savings(request):
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
    