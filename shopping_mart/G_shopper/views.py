from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib import messages
from .form import UserRegistraionForm 
from django.shortcuts import render, redirect
from customAdminPanel.models import *
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your views here.
# def login(request):
#     return render(request, 'register/logged.html', {})

def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if username and password:
            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('G_shopper:home')
            else:
                messages.error(request, "invalid credentials")
        else:
            messages.error(request, 'Please enter correct credentials')
    obj = UserRegistraionForm()
    return render(request, "register/register_form.html", {'form': obj})

def base_page(request):
    return render(request, 'base.html', {})

@login_required(redirect_field_name='user_login', login_url='/userlogin')
def home_page(request):
    products = Product.objects.all()
    return render(request, 'register/home.html', {'obj':products})
  

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



# def products(request):
#     products = Product.objects.all()
#     print(f"\n\n\n\n\nproducts: {products}")
#     return render(request, 'home.html', {'obj':products})