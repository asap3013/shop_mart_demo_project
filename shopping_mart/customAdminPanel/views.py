from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login , logout
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from customAdminPanel.form import *  
from django.views import View


def adminLogin(request):
    if request.user.is_authenticated:
        return redirect('/adminpanel/')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
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

# Forms 


class BannerField(LoginRequiredMixin,View):
    login_url = '/adminpanel/login'
    def get(self,request):
        obj=BannersForm()
        return render(request,"model_form/banner_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=BannersForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:banner')
        else:
            return render(request,"model_form/banner_form.html",{'form':obj})


@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def banner_check(request): 
    fm = Banners.objects.all() 
    context = {'form':fm}
    return render(request,"banner.html",context)
 

    
class DeleteBanner(View):
      def post(self,request):
            data=request.POST
            id=data.get('id')
            fm=Banners.objects.get(id=id)
            fm.delete()
            return redirect('customAdminPanel:banner')    


class EditBanner(View):
    def get (self,request,id):
        print(id)
        obj=Banners.objects.get(id=id)
        fm=BannersForm(instance=obj)
        return render(request,"model_form/editBanner.html",{'form':fm})

    def post(self,request, id):
        ban = Banners.objects.get(id=id)
        fm = BannersForm(request.POST,request.FILES,instance=ban)
        if fm.is_valid():
            fm.save()
            return redirect('customAdminPanel:banner',{})


















  
  
