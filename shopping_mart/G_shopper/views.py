import json
from django.utils.html import strip_tags
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from .form import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from customAdminPanel.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
import random
import stripe
# from django.core.mail import EmailMessage
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.template import Context
# from django.template.loader import get_template
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# User = settings.AUTH_USER_MODEL

# Create your views here.
# def login(request):
#     return render(request, 'register/logged.html', {})


def userLogin(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password1')
        if email and password:
            user = authenticate(username=User.objects.get(email=email).username,password=password)
            if user is not None:
                login(request, user)
                messages.success(request,'User Logged In Successfully')
                return redirect('G_shopper:home')
            else:
                messages.info(request, 'Incorrect Email or Password')
        else:
            messages.info(request, 'Incorrect Email or Password')
    obj = UserRegistraionForm()
    return render(request, "register/login.html", {'form': obj})

# def base_page(request):
#     return render(request, 'base.html', {})


# @csrf_exempt
# @login_required(redirect_field_name='login', login_url='/login')
def home_page(request):
    banners = Banners.objects.all()
    total_data = Product.objects.count()
    products = Product.objects.all().order_by('id')[:3]
    category = Category.objects.all()
    prodcat = ProductCategories.objects.all()
    userWishlist = UserWishList.objects.all()
    userwishlistprod = []
    for i in userWishlist:
        userwishlistprod.append(i.product_id_id)
    # cms = Cms.objects.all()
    context = {'form': banners, 'obj': products,
               'total_data': total_data, 'cat': category, 'prodcat': prodcat,'wishlist':userwishlistprod}
    return render(request, 'register/home.html', context)


def cms_content(request):
    cms = Cms.objects.filter(title='About Us').first()
    cms_title = cms.title
    cms_content = cms.content
    context = {'cms': cms_content,'cms_title':cms_title}
    return render(request, 'about_us.html', context)


def privacy_policy(request):
    cms = Cms.objects.filter(title='Privacy Policy').first()
    cms_content = cms.content
    context = {'cms': cms_content}
    return render(request, 'privacy_policy.html', context)



def logoutuser(request):
    logout(request)
    obj = UserRegistraionForm()
    return render(request, 'register/login.html', {'form': obj})


# @csrf_exempt
# @login_required(redirect_field_name='login', login_url='/login')
# def category_filter(request):
#     breakpoint()
#     category_id = request.GET.get('category_id')
#     request.session['category'] = category_id
#     product_id = ProductCategories.objects.filter(
#         category_id=category_id).values('product_id')
#     product = Product.objects.filter(
#         pk=product_id[0]['product_id']).values('name', 'price')
#     product_img = ProductImages.objects.filter(
#         product_id=product_id[0]['product_id']).values('image_path')
#     return JsonResponse({'product': list(product), 'product_img': list(product_img)})


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def price_filter(request):
    breakpoint()
    category_id = request.GET.get('category_id')
    min_value = request.GET.get('min_price')
    max_value = request.GET.get('max_price')
    if min_value and max_value is not None:
        min_price = int(min_value)
        max_price = int(max_value)
    
    if category_id is not None:
        category_id = request.GET.get('category_id')
        product_id = ProductCategories.objects.filter(category_id=category_id).values('product_id')
        product = Product.objects.filter(pk=product_id[0]['product_id']).values('name', 'price')
        product_img = ProductImages.objects.filter(
            product_id=product_id[0]['product_id']).values('image_path')
        return JsonResponse({'product': list(product), 'product_img': list(product_img)})
    elif category_id is None and min_price<=0 and max_price >=1000:
        product = Product.objects.filter(price__gte=min_price, price__lte=max_price).values(
        'id', 'name', 'price', 'productimages')
        product_img = ProductImages.objects.filter().values('product_id_id', 'image_path')
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
            if i['name'] not in nme:
                nme.append(i['name'])
                continue
        for i in product:
            if i['price'] not in price:
                price.append(i['price'])
                continue
        prods = [nme, price, image]
        return JsonResponse({'product': list(prods)})
    else:
        category_id = request.GET.get('category_id')
        min_value = request.GET.get('min_price')
        max_value = request.GET.get('max_price')
        min_price = int(min_value)
        max_price = int(max_value)
        product = Product.objects.filter(price__gte=min_price, price__lte=max_price).values(
        'id', 'name', 'price', 'productimages')
        product_category = ProductCategories.objects.filter(category_id=category_id).values()
        product_img = ProductImages.objects.filter().values('product_id_id', 'image_path')
        return JsonResponse({'product':list(product),'product_cat': list(product_category),'product_img': list(product_img)})
        
   



# @csrf_exempt
# @login_required(redirect_field_name='login', login_url='/login')
# def price_filter(request):
#     breakpoint()
#     category = request.session['category']
#     min_value = request.GET.get('min_price')
#     max_value = request.GET.get('max_price')
#     min_price = int(min_value)
#     max_price = int(max_value)
#     product = Product.objects.filter(price__gte=min_price, price__lte=max_price).values(
#         'id', 'name', 'price', 'productimages')
#     product_img = ProductImages.objects.filter().values('product_id_id', 'image_path')
#     nme = []
#     price = []
#     image = []
#     prodid = []
#     for i in product:
#         for j in product_img:
#             if int(i['id']) == int(j['product_id_id']):
#                 if j['product_id_id'] not in prodid:
#                     prodid.append(j['product_id_id'])
#                     image.append(j['image_path'])
#                     continue
#     for i in product:
#         if i['name'] not in nme:
#             nme.append(i['name'])
#             continue
#     for i in product:
#         if i['price'] not in price:
#             price.append(i['price'])
#             continue
#     prods = [nme, price, image]
#     return JsonResponse({'product': list(prods)})


# @csrf_exempt
# @login_required(redirect_field_name='login', login_url='/login')
# def filter(request):
#     category_id = request.GET.get('category_id')
#     request.session['category'] = category_id
#     product_id = ProductCategories.objects.filter(category_id=category_id).values('product_id')
#     product = Product.objects.filter(product_id=product_id).values('name','price')
#     product_img = ProductImages.objects.filter(product_id=product).filter('product_id_id', 'image_path')


# @csrf_exempt
# @login_required(redirect_field_name='login', login_url='/login')
# def filter(request):
#     category_id = request.GET.get('category_id')
#     request.session['category'] = category_id
#     product_id = ProductCategories.objects.filter(
#         category_id=category_id).values('product_id')
#     # product = Product.objects.filter(
#     #     pk=product_id[0]['product_id']).values('name', 'price')   
#     min_value = request.GET.get('min_price')
#     max_value = request.GET.get('max_price')
#     min_price = int(min_value)
#     max_price = int(max_value)
#     product_img = ProductImages.objects.filter(
#         product_id=product_id[0]['product_id']).values('product_id_id','image_path')
#     product = Product.objects.filter(price__gte=min_price, price__lte=max_price).values(
#         'id', 'name', 'price', 'productimages')
#     # product_imgs = ProductImages.objects.filter().values('product_id_id', 'image_path')

    
#     nme = []
#     price = []
#     image = []
#     prodid = []
#     for i in product:
#         for j in product_img:
#             if int(i['id']) == int(j['product_id_id']):
#                 if j['product_id_id'] not in prodid:
#                     prodid.append(j['product_id_id'])
#                     image.append(j['image_path'])
#                     continue
#     for i in product:
#         if i['name'] not in nme:
#             nme.append(i['name'])
#             continue
#     for i in product:
#         if i['price'] not in price:
#             price.append(i['price'])
#             continue
#     prods = [nme, price, image]
#     return JsonResponse({'product': list(product), 'product_img': list(product_img),'prods':prods})

class UserRegister(View):
    def get(self, request):
        obj = UserRegistraionForm()
        return render(request, "register/register_form.html", {'form': obj})

    def post(self, request):
        obj = UserRegistraionForm(request.POST)
        user_mail = request.POST['email']
        email_template = EmailTemplate.objects.filter(
            title='User Registration').first()
        if obj.is_valid():
            obj.save()
            # user_mail = obj.__dict__['cleaned_data']['email']
            subject = 'Thanks for Register'
            context = {'data': email_template.content}
            html_message = render_to_string('mail_template.html', context)
            plain_message = strip_tags(html_message)
            # t = loader.get_template('mail_template.html')
            # html = t.render(context={'data':email_template.content})
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_mail, ],
                fail_silently=False,
            )
            messages.success(request, "User Register Successfully")
            return redirect('G_shopper:register')
        else:
            messages.error(request, "invalid Credientials")
            return render(request, "register/register_form.html", {'form': obj})


def mail_template(request):
    email_template = EmailTemplate.objects.filter(
        title='User Registration').first()
    email = email_template.content
    context = {'data': email}
    return render(request, 'mail_template.html', context)


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
# Add to cart
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
    messages.success(request,'Product Added to Cart')
    # messages = 'Product Added to Cart'
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def cart_list(request):
    total_amt = 0
    length = len(request.session['cartdata'])
    if 'cartdata' in request.session:
        for item in request.session['cartdata'].items():
            total_amt += (int(item[1]['qty']))*float(item[1]['price'])

        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt,'length':length})


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
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
@login_required(redirect_field_name='login', login_url='/login')
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


class DeleteCart(View):
    def post(self, request):
        data = request.POST
        id = data.get('id')
        datas = request.session.get("cartdata", {})
        if id in datas:
            del datas[id]  # remove the id
            request.session["cartdata"] = datas
            messages.error(request,"Product Deleted From Cart Successfully")
        return redirect('G_shopper:addcart')



@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
# Wishlist
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = UserWishList.objects.filter(
        product_id=product, user_id=request.user).count()
    
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = UserWishList.objects.create(
            product_id=product,
            user_id=request.user)

        data = {
            'bool': True,

        }
    messages.success(request,'Product Added to Wishlist')
    return JsonResponse(data)


class DeleteWishlist(View):
    def post(self, request):
        data = request.POST
        id = data.get('id')
        fm = UserWishList.objects.get(product_id=id)
        fm.delete()
        messages.error(request,"Product Deleted From Wishlist Successfully")
        return redirect('G_shopper:my_wishlist')


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def my_wishlist(request):
    wlist = UserWishList.objects.filter(user_id=request.user.id).order_by('id')
    count = wlist.count()
    context = {'wlist': wlist,'count':count}
    return render(request, 'wishlist.html', context)

# def deletewishlist(request, id):
#     user=request.user.id
#     UserWishList.objects.filter(user_id=user.id, product=Product.objects.get(id=id).delete())
#     UserWishList.delete()
#     return HttpResponseRedirect('/my-wishlist')


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'productDetails.html', {'product': product})


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def couponcalculate(request):
    data = {
        'id': '',
        'coupon_code': '',
        'percent_off': '',
    }
    pid = request.GET['cart_coupon']
    coupon = Coupon.objects.all().values('pk', 'code', 'percent_off')
    for i in coupon:
        if (i['code'] == pid):
            data['id'] = i['pk']
            data['percent_off'] = i['percent_off']
            data['coupon_code'] = i['code']
            request.session['coupon_data'] = data
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def checkout(request):
    address = UserAddress.objects.all()
    # request.session['address'] = address
    total_amt = 0
    if 'cartdata' in request.session:
        for item in request.session['cartdata'].items():
            total_amt += (int(item[1]['qty']))*float(item[1]['price'])
        return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'address': address})
    else:
        return render(request, 'checkout.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt, 'address': address})


class Add_address(View):
    def get(self, request):
        obj = Address_form()
        return render(request, "register/address_form.html", {'form': obj})

    def post(self, request):
        obj = Address_form(request.POST, user=request.user)
        if obj.is_valid():
            obj.save()
            msg = 'Address added successfully'
            return redirect('G_shopper:addcart', {'msg': msg})
        else:
            msg = 'Check details'
            return render(request, "register/address_form.html", {'form': obj, 'msg': msg})


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def placeorder(request):
    cart = request.session['cartdata']
    coupon = request.session['coupon_data']
    address_id = request.session['address_id']
    address = UserAddress.objects.get(pk=address_id)
    final_amount = request.session['final_total']
    ship_amount = request.session['ship_amount']

    order = UserOrder(
        user_id=request.user,
        transaction_id=random.random()*100000000000000000,
        shipping_charges=ship_amount,
        coupon_id_id=coupon['id'],
        billing_address_1=address.address_1,
        billing_address_2=address.address_2,
        billing_city=address.city,
        billing_state=address.state,
        billing_country=address.country,
        billing_zipcode=address.zip_code,
        shipping_address_1=address.address_1,
        shipping_address_2=address.address_2,
        shipping_city=address.city,
        shipping_country=address.country,
        shipping_zipcode=address.zip_code,
        grand_total=final_amount,
    )
    order.save()
    order_ids = order.id
    messages.success(request, "Order placed Successfully")
    if order.save:
        order_id = order_ids
        cart_details = request.session['cartdata']
        for key, value in cart_details.items():
            print(value)
            order_details = OrderDetails(
                order_id=order_id,
                product_id_id=key,
                amount=cart_details[key]['price'],
                quantity=cart_details[key]['qty']
            )
            order_details.save()
        user_email = request.user.email
        email_template = EmailTemplate.objects.filter(
            title='Order placed').first()
        subject = 'Order Placed Successfully'
        context = {'data': email_template.content,
                   'order_details': order_details}
        html_message = render_to_string('order_mail_template.html', context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
    messages.success(request,'Order Placed Successfully')
    return redirect('G_shopper:home')


def order_mail_template(request):
    email_template = EmailTemplate.objects.filter(title='Order placed').first()
    email = email_template.content
    context = {'data': email}
    return render(request, 'order_mail_template.html', context)


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
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
        unit_amount_decimal=total * 100,
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

        success_url='http://127.0.0.1:8000' + '/placeorder',
        cancel_url='http://localhost:8000' + '/cancel.html',
    )

    return JsonResponse(checkout_session.url, safe=False)


@csrf_exempt
def cashondelivery(request):
    cart = request.session['cartdata']
    # user_email = User.objects.first()
    coupon = request.session['coupon_data']
    address_id = request.POST.get('address_id')
    address = UserAddress.objects.get(pk=address_id)
    final_amount = request.POST.get('TOTAL')
    ship_amount = request.POST.get('ship_amt')

    order = UserOrder(
        user_id=request.user,
        transaction_id=random.random()*100000000000000000,
        shipping_charges=ship_amount,
        coupon_id_id=coupon['id'],
        billing_address_1=address.address_1,
        billing_address_2=address.address_2,
        billing_city=address.city,
        billing_state=address.state,
        billing_country=address.country,
        billing_zipcode=address.zip_code,
        shipping_address_1=address.address_1,
        shipping_address_2=address.address_2,
        shipping_city=address.city,
        shipping_country=address.country,
        shipping_zipcode=address.zip_code,
        grand_total=final_amount
    )
    order.save()
    order_ids = order.id
    if order.save:
        order_id = order_ids
        cart_details = request.session['cartdata']
        for key, value in cart_details.items():
            print(value)
            order_details = OrderDetails(
                order_id=order_id,
                product_id_id=key,
                amount=cart_details[key]['price'],
                quantity=cart_details[key]['qty']
            )
            order_details.save()

        user_email = request.user.email
        email_template = EmailTemplate.objects.filter(
            title='Order placed').first()
        subject = 'Order Placed Successfully'
        context = {'data': email_template.content,
                   'order_details': order_details}
        html_message = render_to_string('order_mail_template.html', context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
    messages.success(request,'Order Placed Successfully')
    return redirect('G_shopper:home')


@login_required(redirect_field_name='login', login_url='/login')
def tracking_order(request):
    return render(request, 'track_order.html')


def check_order(request):
    order_id = request.POST.get('order_id')
    print(order_id)
    user_order = UserOrder.objects.filter(id=order_id).values('id', 'status').first()
    if user_order:
        # if int(order_id) == user_order['id']:
        status = user_order['status']
        context = {'status': status}
        return render(request, 'order_status.html', context)
    else:
        msg = 'Invalid Order Id'
        return render(request, 'track_order.html', {'msg': msg})


@csrf_exempt
def contact_us(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data["email"]
            message = form.cleaned_data['message']
            form.save()
            try:
                send_mail('Feedback', message, email, [
                          "abhisapkal3013.com"], fail_silently=False)
            except BadHeaderError:
                return HttpResponse(" found.")
            return redirect('G_shopper:contact')
        else:
            print(form.errors)
            return render(request,'contact_us.html',{'form':form})
    return render(request, "contact_us.html", {})


@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def my_order(request):
    order_data = OrderDetails.objects.all()
    image = ProductImages.objects.filter(
        product_id=order_data[0].product_id_id)
    c = []
    d = {}
    for i in order_data:
        d['order_id'] = i.order_id
        d['product_id'] = i.product_id
        d['quantity'] = i.quantity
        d['amount'] = i.amount
        d['image_path'] = ProductImages.objects.filter(
            product_id=i.product_id_id).first().image_path
        c.append(d)
        d = {}
    context = {'order_data': c}
    return render(request, 'my_order.html', context)

# def detailed_order(request,id):
    
    # return render(request, 'order_detailed_page.html', context)

class detailed_order(View):
    """_summary_

    Args:
        View (_type_): _description_
    """

    def get(self, request, order_id):
        order_data = OrderDetails.objects.filter(order_id=order_id).first()
        user_order = UserOrder.objects.filter(id=order_id).first()
        image = ProductImages.objects.filter(product_id=order_data.product_id_id)
        # context = {'form': order_data,'image':image}
        return render(request, "order_detailed_page.html", {'form': order_data,'image':image,'order':user_order})

    def post(self, request, order_id):
        order_data = OrderDetails.objects.filter(order_id=order_id).first()
        image = ProductImages.objects.filter(product_id=order_data.product_id_id)
        return redirect(request,'G_shopper:detailed_order')



@csrf_exempt
@login_required(redirect_field_name='login', login_url='/login')
def my_account(request):
    username = request.user.username
    user_email = request.user.email
    user_first_name = request.user.first_name
    user_last_name = request.user.last_name
    user_address = UserAddress.objects.all()
    context = {'users': username, 'user_email': user_email,
               'first_name': user_first_name, 'last_name': user_last_name, 'address': user_address}
    return render(request, 'my_account.html', context)


def edit_profile(request):
    msg = None
    if request.method == 'POST':
        form = Updateuser_form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Data has been saved'
        else:
            msg = 'Username already taken'
    form = Updateuser_form(instance=request.user)
    return render(request, 'update_user.html', {'form': form, 'msg': msg})


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('G_shopper:password_success')

# view for password success of user.


def password_success(request):
    """
    :param request:
    :return: password success page:
    """
    return render(request, 'password_success.html', {})


def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('id')[offset:offset+limit]
    t = render_to_string('register/products_list.html', {'data': data})
    return JsonResponse({'data': t})



