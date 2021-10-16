from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='finFreedom'
urlpatterns = [
    path('', views.login, name='login'),
    path('overview/', views.overview, name='overview')
]