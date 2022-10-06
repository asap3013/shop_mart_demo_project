from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .form import UserRegistraionForm 
from django.shortcuts import render, redirect
from customAdminPanel.models import *
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your views here.
# def login(request):
#     return render(request, 'register/logged.html', {})

def userLogin(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
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

# def base_page(request):
#     return render(request, 'base.html', {})

@login_required(redirect_field_name='register', login_url='/registration')
def home_page(request):
    products = Product.objects.all()
    return render(request, 'register/home.html', {'obj':products})

def logoutuser(request):
    logout(request)
    obj = UserRegistraionForm()
    return render(request, 'register/register_form.html',{'form': obj} )
  

class UserRegister(View):
    def get(self, request):
        obj = UserRegistraionForm()
        return render(request, "register/register_form.html", {'form': obj})

    def post(self, request):
        obj = UserRegistraionForm(request.POST)
        if obj.is_valid():
            obj.save()
            return redirect('G_shopper:home')
        else: 
            return render(request, "register/register_form.html", {'form': obj})


def add_cart(request):
    # del request.session['cartdata']
	cart_p={}
	cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		# 'price':request.GET['price'],
	}
	if 'cartdata' in request.session:
		if str(request.GET['id']) in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
			cart_data.update(cart_data)
			request.session['cartdata']=cart_data
		else:
			cart_data=request.session['cartdata']
			cart_data.update(cart_p)
			request.session['cartdata']=cart_data
	else:
		request.session['cartdata']=cart_p
	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})


def cart_list(request):
	# total_amt=0
	# if 'cartdata' in request.session:
	# 	for p_id,item in request.session['cartdata'].items():
	# 		total_amt+=int(item['qty'])*float(item['price'])
    return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
	# else:
	# 	return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# def add_to_cart(request, product_id):
#     cart = request.session.get('cart', {})
#     product = Product.objects.get(id=product_id)
#     cart[product_id] = product
#     request.session['cart'] = cart
#     return redirect(request("cart"))


# # Cart View
# def get_cart(request):
#     cart = request.session.get('cart',{})
#     return render(request, 'cart.html', cart)