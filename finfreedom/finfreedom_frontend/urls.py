from django.contrib import auth
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('overview/', views.overview, name='overview'),
    path('manage/', views.manage, name='manage'),
    path('transactions/', views.transactions, name='transactions'),
    path('subscriptions/', views.subscriptions,name='subscriptions'),
    path('accounts/', views.accounts, name='accounts'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),

    #reset password django paths
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="login/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="login/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="login/reset_password_done.html"), name="password_reset_complete"),

    #POST Calls
    path('create_account/', views.create_account, name="create_acount"),
]