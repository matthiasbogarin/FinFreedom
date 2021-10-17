from django.contrib import auth
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('check_if_email_exists/', views.check_if_email_exists, name="check_if_email_exists"),
]