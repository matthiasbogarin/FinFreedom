from django.contrib import auth
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('check_if_email_exists/', views.check_if_email_exists, name="check_if_email_exists"),
    path('check_if_passwords_match/', views.check_if_passwords_match, name="check_if_passwords_match"),

    #Api Calls
    # path('create_account/', views.create_account, name="create_account"),
]