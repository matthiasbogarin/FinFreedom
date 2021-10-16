from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='finFreedom'
urlpatterns = [
    path('', views.login, name='login'),
    path('overview/', views.overview, name='overview'),
    path('manage/', views.manage, name='manage'),
    path('transactions/', views.transactions, name='transactions'),
    path('subscriptions/', views.subscriptions,name='subscriptions'),
    path('accounts/', views.accounts, name='accounts'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]