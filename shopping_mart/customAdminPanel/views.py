from re import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login , logout
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate
from django.contrib import messages



def adminLogin(request):
    if request.user.is_authenticated:
        return redirect('/adminpanel/')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        # print("user","pass",username,password)
        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('customAdminPanel:index')
            else:
                messages.error(request,"invalid credentials")
        else:
            messages.error(request, 'Please enter correct credentials')
        
    return render(request,'login.html',{})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def index(request):
    return render(request,'starter.html',{})
 
def logoutUser(request):
    logout(request)
    return render(request,'login.html',{})
































  
  
