from django.shortcuts import redirect, render

# Create your views here.

def login(request):
    print("Reached the Login Page")
    return render(request, 'login/login.html')