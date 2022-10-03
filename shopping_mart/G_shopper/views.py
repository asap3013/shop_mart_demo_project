from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from .form import UserRegistraionForm 
from django.shortcuts import render, redirect

from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your views here.
# def login(request):
#     return render(request, 'register/logged.html', {})

def userLogin(request):

    if request.user.is_authenticated:
        breakpoint()
        return redirect('/user/')

    if request.method == 'POST':
        breakpoint()
        username = request.POST('username')
        password = request.POST('password1')
        if username and password:
            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('G_shopper:base')
            else:
                messages.error(request, "invalid credentials")
        else:
            messages.error(request, 'Please enter correct credentials')

    return render(request, 'register/register_form.html', {})

def base_page(request):
    return render(request, 'base.html', {})
  

class UserRegister(View):
    def get(self, request):
        obj = UserRegistraionForm()
        return render(request, "register/register_form.html", {'form': obj})

    def post(self, request):
        obj = UserRegistraionForm(request.POST)
        if obj.is_valid():
            obj.save()
            return redirect('G_shopper:base')
        else: 
            return render(request, "register/register_form.html", {'form': obj})
