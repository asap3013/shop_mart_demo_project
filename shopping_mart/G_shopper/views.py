from multiprocessing import context
from unicodedata import category
import json
from django.core import serializers
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .form import *
from django.shortcuts import render, redirect
from customAdminPanel.models import *
from django.http import JsonResponse 
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
import random
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def home_page(request):
    banners = Banners.objects.all()
    products = Product.objects.all()
    category = Category.objects.all()
    prodcat = ProductCategories.objects.all()

    context={'form':banners,'obj':products,'cat':category,'prodcat':prodcat}
    return render(request, 'register/home.html',context)


def logoutuser(request):
    logout(request)
    obj = UserRegistraionForm()
    return render(request, 'register/register_form.html', {'form': obj})


def category_filter(request):
    category_id = request.GET.get('category_id')
    request.session['category'] = category_id
    product_id = ProductCategories.objects.filter(category_id=category_id).values('product_id')
    product = Product.objects.filter(pk = product_id[0]['product_id']).values('name','price')
    product_img = ProductImages.objects.filter(product_id=product_id[0]['product_id']).values('image_path')
    return JsonResponse({'product':list(product),'product_img':list(product_img)})

def price_filter(request):
    minvalue = request.GET.get('minvalue') 
    maxvalue = request.GET.get('maxvalue')
    return JsonResponse({'minvalue':list(minvalue),'maxvalue':list(maxvalue)})
    

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
    wlist = UserWishList.objects.filter(user_id=request.user.id).order_by('id')
    return render(request, 'wishlist.html', {'wlist': wlist})

# def deletewishlist(request, id):
#     breakpoint()
#     user=request.user.id
#     UserWishList.objects.filter(user_id=user.id, product=Product.objects.get(id=id).delete())
#     UserWishList.delete()
#     return HttpResponseRedirect('/my-wishlist')

def product_detail(request,product_id):
    product = Product.objects.get(id=product_id)
    return render(request,'productDetails.html',{'product':product})

def couponcalculate(request):
    data={
        'id':'',
        'coupon_code':'',
        'percent_off':'',
    }
    pid = request.GET['cart_coupon']
    coupon = Coupon.objects.all().values('pk','code','percent_off')
    for i in coupon:
        if (i['code']==pid):
            data['id']=i['pk'] 
            data['percent_off']=i['percent_off']
            data['coupon_code']=i['code'] 
            request.session['coupon_data']=data
    return JsonResponse(data,safe=False)


def checkout(request):
    address = UserAddress.objects.all()
    # request.session['address'] = address
    total_amt = 0
    if 'cartdata' in request.session:
        for item in request.session['cartdata'].items():
            total_amt += (int(item[1]['qty']))*float(item[1]['price'])
        return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt,'address':address})
    else:
        return render(request, 'checkout.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt,'address':address})


class Add_address(View):
    def get(self, request):
        obj = Address_form()
        return render(request, "register/address_form.html", {'form': obj})

    def post(self, request):
        obj = Address_form(request.POST)
        if obj.is_valid():
            obj.save()
            return redirect('G_shopper:addcart')
        else:
            return render(request, "register/address_form.html", {'form': obj})

@csrf_exempt  
def placeorder(request):
    cart = request.session['cartdata'] 
    coupon = request.session['coupon_data'] 
    address_id = request.session['address_id']
    address = UserAddress.objects.get(pk=address_id)
    final_amount = request.session['final_total']
    ship_amount = request.session['ship_amount']

    order = UserOrder(
            user_id = request.user,
            transaction_id = random.random()*100000000000000000,
            shipping_charges = ship_amount,
            coupon_id_id = coupon['id'],
            billing_address_1 = address.address_1,
            billing_address_2 = address.address_2,
            billing_city = address.city,
            billing_state = address.state,
            billing_country = address.country,
            billing_zipcode = address.zip_code,
            shipping_address_1 = address.address_1,
            shipping_address_2 = address.address_2,
            shipping_city = address.city,
            shipping_country = address.country,
            shipping_zipcode = address.zip_code,
            grand_total = final_amount,
        )
    order.save()
    return redirect('G_shopper:home')

@csrf_exempt
def stripe_order(request):
    breakpoint
    cart = request.session['cartdata'] 
    coupon = request.session['coupon_data'] 
    json_data = json.loads(request.body.decode("utf-8"))
    address_id = json_data.get('address_id')
    request.session['address_id'] = address_id
    total = float(json_data.get('total'))
    print(total)
    print(type(total))
    request.session['final_total'] = total
    ship_amount = json_data.get('ship_amount')
    request.session['ship_amount'] = ship_amount

    stripe.api_key = "sk_test_51LsPV8SFVCTJbUjWsE8cslsMCnNNp3PUS7mQIoUAzsgKKFaMokZ5rIXaLyiSUSPgOpcZTD02FGjDMgFXOwjrHY7200sqNGxgu1"
    product = stripe.Product.create(name="product")
    
    price = stripe.Price.create(
            unit_amount_decimal = total * 100 ,
            currency="INR",
            product=product.id,
            )
    checkout_session = stripe.checkout.Session.create(
       
        line_items=[
            {
            'price': price.id,
            'quantity': 1,
            
            },
        ],
        
        mode='payment',
        
        success_url= 'http://127.0.0.1:8000' + '/placeorder',
        cancel_url= 'http://localhost:8000' + '/cancel.html',
        )
    
    return JsonResponse(checkout_session.url,safe=False)

@csrf_exempt
def cashondelivery(request):
    cart = request.session['cartdata'] 
    coupon = request.session['coupon_data'] 
    address_id = request.GET.get('address_id')
    address = UserAddress.objects.get(pk=address_id)
    final_amount = request.session['final_total']
    ship_amount = request.session['ship_amount']

    order = UserOrder(
            user_id = request.user,
            transaction_id = random.random()*100000000000000000,
            shipping_charges = ship_amount,
            coupon_id_id = coupon['id'],
            billing_address_1 = address.address_1,
            billing_address_2 = address.address_2,
            billing_city = address.city,
            billing_state = address.state,
            billing_country = address.country,
            billing_zipcode = address.zip_code,
            shipping_address_1 = address.address_1,
            shipping_address_2 = address.address_2,
            shipping_city = address.city,
            shipping_country = address.country,
            shipping_zipcode = address.zip_code,
            grand_total = final_amount
        )
    order.save()
    return redirect('G_shopper:home')






    


