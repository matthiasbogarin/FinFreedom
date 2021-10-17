# from django.shortcuts import render
# from .models import *

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


def check_if_email_exists(request):
    email = request.GET['email']
    list_of_emails = User.objects.filter(email=email).values('email')
    for item in list_of_emails:
        if(item['email'] == email):
            print("true")
            return JsonResponse({ "exists" : True})
        else:
            print("false")
        
    return JsonResponse({ "exists" : False})

def check_if_passwords_match(request):
    new_password = request.GET['new_password']
    verify_password = request.GET['verify_password']
    if(new_password == verify_password):
        return JsonResponse({ "matched" : True})
    else:
        return JsonResponse({ "matched" : False})

def create_account(request):
    print("Request: ", request.POST)
    return None
        
