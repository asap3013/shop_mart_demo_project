from multiprocessing import context
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .form import UserRegistraionForm
from django.shortcuts import render, redirect
from customAdminPanel.models import *
from django.http import JsonResponse , HttpResponseRedirect
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
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
            user = authenticate(request, username=username, password=password)

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
    banners = Banners.objects.all()
    products = Product.objects.all()
    context={'form':banners,'obj':products}
    return render(request, 'register/home.html',context)


def logoutuser(request):
    logout(request)
    obj = UserRegistraionForm()
    return render(request, 'register/register_form.html', {'form': obj})


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

#Add to cart
def add_cart(request):
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


def cart_list(request):
    total_amt = 0
    if 'cartdata' in request.session:
        for item in request.session['cartdata'].items():
            total_amt += (int(item[1]['qty']))*float(item[1]['price'])

        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})


def delete_cart_item(request):
    prod_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if prod_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][prod_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for prod_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Wishlist
def add_wishlist(request):
    breakpoint()
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = UserWishList.objects.filter(product_id=product, user_id=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = UserWishList.objects.create(
            product_id=product,
            user_id=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)

def my_wishlist(request):
    # breakpoint()
    wlist = UserWishList.objects.filter(user_id=request.user.id).order_by('id')
    return render(request, 'wishlist.html', {'wlist': wlist})

# def deletewishlist(request, id):
#     breakpoint()
#     user=request.user.id
#     UserWishList.objects.filter(user_id=user.id, product=Product.objects.get(id=id).delete())
#     UserWishList.delete()
#     return HttpResponseRedirect('/my-wishlist')

def product_detail(request,id):
    product = Product.objects.filter(id=id).first()
    context={
        'product':product
    }
    return render(request,'productDetails.html',context)

def couponcalculate(request):
    data=[]
    pid = request.GET['cart_coupon']
    coupon = Coupon.objects.all().values('code','percent_off')
    for i in coupon:
        if (i['code']==pid):
            data.append(i['percent_off'])
    return JsonResponse(data,safe=False)





    
    



    


