from multiprocessing import context
from unicodedata import category
import json
from django.shortcuts import render
from django.core.mail import send_mail ,BadHeaderError
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .form import *
from django.shortcuts import render, redirect
from customAdminPanel.models import *
from django.http import HttpResponse,JsonResponse 
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
# from forms import PasswordChangingForm
import random
import stripe
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
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

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def category_filter(request):
    category_id = request.GET.get('category_id')
    request.session['category'] = category_id
    product_id = ProductCategories.objects.filter(category_id=category_id).values('product_id')
    product = Product.objects.filter(pk = product_id[0]['product_id']).values('name','price')
    product_img = ProductImages.objects.filter(product_id=product_id[0]['product_id']).values('image_path')

    return JsonResponse({'product':list(product),'product_img':list(product_img)})

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def price_filter(request):
    min_value = request.GET.get('min_price') 
    max_value = request.GET.get('max_price')
    min_price = int(min_value)
    max_price = int(max_value)
    product = Product.objects.filter(price__gte=min_price, price__lte=max_price).values('id','name','price','productimages')
    product_img = ProductImages.objects.filter().values('product_id_id','image_path')
    nme = []
    price = []
    image = []
    prodid = []
    for i in product:
        for j in product_img:
            if int(i['id']) == int(j['product_id_id']):
                if j['product_id_id'] not in prodid:
                    prodid.append(j['product_id_id'])
                    image.append(j['image_path'])
                    continue
    for i in product:
        if i['name'] not in nme :
            nme.append(i['name'])
            continue
    for i in product:
        if i['price'] not in price:
            price.append(i['price'])
            continue
    prods = [nme,price,image]
    return JsonResponse({'product':list(prods)})
    

class UserRegister(View):
    def get(self, request):
        obj = UserRegistraionForm()
        return render(request, "register/register_form.html", {'form': obj})

    def post(self, request):
        obj = UserRegistraionForm(request.POST)
        if obj.is_valid():
            obj.save()
            user_mail = obj.__dict__['cleaned_data']['email']
            send_mail(
            'Thanks for Register',
            'HEY you are now successfully register in our e-shopper website',
            settings.EMAIL_HOST_USER,
            [user_mail],
            fail_silently=False,
            )
            messages.success(request, "User Register Successfully")
            return redirect('G_shopper:home')
        else:
            messages.error("invalid Credientials")
            return render(request, "register/register_form.html", {'form': obj})


@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
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

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def cart_list(request):
    total_amt = 0

    if 'cartdata' in request.session:
        for item in request.session['cartdata'].items():
            total_amt += (int(item[1]['qty']))*float(item[1]['price'])

        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def delete_cart_item(request):
    prod_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if prod_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            # del request.session['cartdata'][prod_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for prod_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    context = {'total_amt': total_amt}
    return JsonResponse({'data': context, 'totalitems': len(request.session['cartdata'])})

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
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
    context = {'total_amt': total_amt}
    return JsonResponse({'data': context, 'totalitems': len(request.session['cartdata'])})

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
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

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def my_wishlist(request):
    wlist = UserWishList.objects.filter(user_id=request.user.id).order_by('id')
    return render(request, 'wishlist.html', {'wlist': wlist})

# def deletewishlist(request, id):
#     user=request.user.id
#     UserWishList.objects.filter(user_id=user.id, product=Product.objects.get(id=id).delete())
#     UserWishList.delete()
#     return HttpResponseRedirect('/my-wishlist')

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def product_detail(request,product_id):
    product = Product.objects.get(id=product_id)
    return render(request,'productDetails.html',{'product':product})


@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
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

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
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
        obj = Address_form(request.POST,user = request.user)
        if obj.is_valid():
            obj.save()
            return redirect('G_shopper:addcart')
        else:
            return render(request, "register/address_form.html", {'form': obj})
@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
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
    order_ids = order.id
    if order.save:
        order_id = order_ids
        cart_details = request.session['cartdata']
        for key,value in cart_details.items():
            print(value)
            order_details = OrderDetails(
                order_id = order_id,
                product_id_id = key,
                amount = cart_details[key]['price'],
                quantity = cart_details[key]['qty']
            )
            order_details.save()
    user_email = request.user.email
    send_mail(
            'Thank You for Order',
            'HEY you are now successfully placed your order in our E-shopper website',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
            )
    cart.clear()
    return redirect('G_shopper:home')

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
@csrf_exempt
def stripe_order(request):
    cart = request.session['cartdata'] 
    coupon = request.session['coupon_data'] 
    json_data = json.loads(request.body.decode("utf-8"))
    address_id = json_data.get('address_id')
    request.session['address_id'] = address_id
    total = float(json_data.get('total'))
    request.session['final_total'] = total
    final_total = request.session['final_total']
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
@login_required(redirect_field_name='register', login_url='/registration')
def cashondelivery(request):
    cart = request.session['cartdata'] 
    # user_email = User.objects.first()
    coupon = request.session['coupon_data'] 
    address_id = request.POST.get('address_id')
    address = UserAddress.objects.get(pk=address_id)
    final_amount = request.POST.get('TOTAL')
    ship_amount = request.POST.get('ship_amt')

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
    order_ids = order.id
    if order.save:
        order_id = order_ids
        cart_details = request.session['cartdata']
        for key,value in cart_details.items():
            print(value)
            order_details = OrderDetails(
                order_id = order_id,
                product_id_id = key,
                amount = cart_details[key]['price'],
                quantity = cart_details[key]['qty']
            )

            order_details.save()
    # user_email =  request.user.email
    # # order = instance
    # context = {'order': order}
    # message = get_template("product_order.html").render(context)
    # mail = EmailMessage(
    #     subject="Order confirmation",
    #     body=message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     to=[user_email],
    #     # reply_to=[user_email],
    # )
    # mail.content_subtype = "html"
    # return mail.send()
    user_email =  request.user.email
    send_mail(
            'Thank You for Order',
            'HEY you are now successfully placed your order in our E-shopper website',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
            )
    subject = 'Thank You for Order'
    html_message = render_to_string('product_order.html', {'context': 'values'})
    # plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = [user_email]
    request.session['cartdata'].clear()
    return redirect('G_shopper:home')



@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def tracking_order(request):
    email_id = request.POST.get('email')
    order_id = request.POST.get('order_id')
    # order = int(order_id)
    user_email =request.user.email
    user_order = UserOrder.objects.filter(user_id__email=email_id, id=order_id).values('id','status').first()
    if email_id == user_email and  int(order_id) == user_order['id']:
        status = user_order['status']
        context = {'status':status}
        return render(request,'order_status.html',context)
    else:
        messages.error(request, 'Please enter correct credentials')
    return render(request,'track_order.html')


@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def contact_us(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            email = form.cleaned_data["email"]
            message = form.cleaned_data['message']
            form.save()
            try:
                send_mail('Feedback',message, email, ["abhisheksapkal1316@gmail.com"],fail_silently=False)
            except BadHeaderError:
                return HttpResponse(" found.")
        return redirect('G_shopper:contact')
    return render(request,"contact_us.html",{})

@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def my_order(request):
    order_data = OrderDetails.objects.all()
    context={'order_data':order_data}
    return render(request,'my_order.html',context)


@csrf_exempt
@login_required(redirect_field_name='register', login_url='/registration')
def my_account(request):
    username = request.user.username
    user_email = request.user.email
    context = {'users':username,'user_email':user_email}
    return render(request,'my_account.html',context)



class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('G_shopper:password_success')

# view for password success of user.
def password_success(request):
    """
    :param request:
    :return: password success page:
    """
    return render(request, 'password_success.html',{})
