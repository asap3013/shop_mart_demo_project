from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login , logout
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from customAdminPanel.form import *  
from django.views import View


def adminLogin(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        View (_type_): _description_
    """
    def get (self,request,id):
        obj=Banners.objects.get(id=id)
        fm=BannersForm(instance=obj)
        return render(request,"model_form/editBanner.html",{'form':fm})

    def post(self,request, id):
        ban = Banners.objects.get(id=id)
        fm = BannersForm(request.POST,request.FILES,instance=ban)
        if fm.is_valid():
            fm.save()
            return redirect('customAdminPanel:banner',{})

# class CategoryField(LoginRequiredMixin,View):
#     login_url = '/adminpanel/login'
#     def get(self,request):
#         obj=CategoryForm()
#         return render(request,"model_form/category_form.html",{'form':obj})
#     # @login_required
#     def post(self,request):
#         obj=CategoryForm(request.POST)
#         if obj.is_valid():
#             obj.save()
#             # print(instance.name)
#             return redirect('customAdminPanel:category')
#         else:
#             return render(request,"model_form/category_form.html",{'form':obj})

# @login_required(redirect_field_name='login', login_url='/adminpanel/login')
# def category_check(request): 
#     fm = Category.objects.all() 
#     context = {'form':fm}
#     return render(request,"category.html",context)


class CategoryField(View):   
    def get(self,request):
        obj=CategoryForm()
        return render(request,"model_form/category_form.html",{'form':obj})
    def post(self,request):
        obj=CategoryForm(request.POST)
        if obj.is_valid():
            obj.save()
            return redirect('customAdminPanel:category')
        else:
            return render(request,"model_form/category_form.html",{'form':obj})
@login_required(redirect_field_name='login',login_url='/adminpanel/login')
def category_check(request):
      obj=Category.objects.all()
      keys={"obj":obj}
      return render(request,"category.html",keys)



class CmsField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=CmsForm()
        return render(request,"model_form/cms_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=CmsForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:cms')
        else:
            return render(request,"model_form/cms_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def cms_check(request): 
    fm = Cms.objects.all() 
    context = {'form':fm}
    return render(request,"cms.html",context)


class ContactUsField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ContactUsForm()
        return render(request,"model_form/contactUs_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ContactUsForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:contactUs')
        else:
            return render(request,"model_form/contactUs_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def contactUs_check(request): 
    fm = ContactUs.objects.all() 
    context = {'form':fm}
    return render(request,"contactUs.html",context)




class CouponField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=CouponForm()
        return render(request,"model_form/coupon_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=CouponForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:coupon')
        else:
            return render(request,"model_form/coupon_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def coupon_check(request): 
    fm = Coupon.objects.all() 
    context = {'form':fm}
    return render(request,"coupon.html",context)


    

class ConfigurationField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ConfigurationForm()
        return render(request,"model_form/configuration_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ConfigurationForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:configuration')
        else:
            return render(request,"model_form/configuration_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def configuration_check(request): 
    fm = Configuration.objects.all() 
    context = {'form':fm}
    return render(request,"configuration.html",context)



class EmailField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=EmailTemplateForm()
        return render(request,"model_form/email_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=EmailTemplateForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:email')
        else:
            return render(request,"model_form/email_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def email_check(request): 
    fm = EmailTemplate.objects.all() 
    context = {'form':fm}
    return render(request,"email.html",context)



class OrderDetailField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=OrderDetailsForm()
        return render(request,"model_form/orderDetail_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=OrderDetailsForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:orderDetail')
        else:
            return render(request,"model_form/orderDetail_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def orderDetail_check(request): 
    fm = OrderDetails.objects.all() 
    context = {'form':fm}
    return render(request,"orderDetail.html",context)

  
class PaymentGatewayField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=PaymentGatewayForm()
        return render(request,"model_form/paymentGateway_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=PaymentGatewayForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:paymentGateway')
        else:
            return render(request,"model_form/paymentGateway_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def paymentGateway_check(request): 
    fm = PaymentGateway.objects.all() 
    context = {'form':fm}
    return render(request,"paymentGateway.html",context)



class ProductField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ProductForm()
        return render(request,"model_form/product_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ProductForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:product')
        else:
            return render(request,"model_form/product_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def product_check(request): 
    fm = Product.objects.all() 
    context = {'form':fm}
    return render(request,"product.html",context)



class ProductAttributesField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ProductAttributesForm()
        return render(request,"model_form/productAttributes_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ProductAttributesForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:productAttributes')
        else:
            return render(request,"model_form/productAttributes_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def productAttributes_check(request): 
    fm = ProductAttributes.objects.all() 
    context = {'form':fm}
    return render(request,"productAttributes.html",context)




class ProductAttributesAssocField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ProductAttributesAssocForm()
        return render(request,"model_form/productAttributesAssoc_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ProductAttributesAssocForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:productAttributesAssoc')
        else:
            return render(request,"model_form/productAttributesAssoc_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def productAttributesAssoc_check(request): 
    fm = ProductAttributesAssoc.objects.all() 
    context = {'form':fm}
    return render(request,"productAttributesAssoc.html",context)


class ProductAttributesValuesField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ProductAttributesValuesForm()
        return render(request,"model_form/productAttributesValues_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ProductAttributesValuesForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:productAttributesValues')
        else:
            return render(request,"model_form/productAttributesValues_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def productAttributesValues_check(request): 
    fm = ProductAttributesValues.objects.all() 
    context = {'form':fm}
    return render(request,"productAttributesValues.html",context)


class ProductCategoryField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ProductCategoryForm()
        return render(request,"model_form/productCategory_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ProductCategoryForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:productCategory')
        else:
            return render(request,"model_form/productCategory_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def productCategory_check(request): 
    fm = ProductCategories.objects.all() 
    context = {'form':fm}
    return render(request,"productCategory.html",context)


class ProductImagesField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=ProductImagesForm()
        return render(request,"model_form/productImages_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=ProductImagesForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:productImages')
        else:
            return render(request,"model_form/productImages_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def productImages_check(request): 
    fm = ProductImages.objects.all() 
    context = {'form':fm}
    return render(request,"productImages.html",context)



class UsedCouponField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=UsedCouponForm()
        return render(request,"model_form/usedCoupon_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=UsedCouponForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:usedCoupon')
        else:
            return render(request,"model_form/usedCoupon_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def usedCoupon_check(request): 
    fm = CouponsUsed.objects.all() 
    context = {'form':fm}
    return render(request,"usedCoupon.html",context)




class UserField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=UserForm()
        return render(request,"model_form/user_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=UserForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:user')
        else:
            return render(request,"model_form/user_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def user_check(request): 
    fm = User.objects.all() 
    context = {'form':fm}
    return render(request,"user.html",context)

class UserAddressField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=UserAddressForm()
        return render(request,"model_form/userAddress_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=UserAddressForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:userAddress')
        else:
            return render(request,"model_form/userAddress_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def userAddress_check(request): 
    fm = UserAddress.objects.all() 
    context = {'form':fm}
    return render(request,"userAddress.html",context)


class UserOrderField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=UserOrderForm()
        return render(request,"model_form/userOrder_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=UserOrderForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:userOrder')
        else:
            return render(request,"model_form/userOrder_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def userOrder_check(request): 
    fm = UserOrder.objects.all() 
    context = {'form':fm}
    return render(request,"userOrder.html",context)


class UserWishlistField(LoginRequiredMixin,View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_

    Returns:
        _type_: _description_
    """

    login_url = '/adminpanel/login'
    def get(self,request):
        obj=UserWishlistForm()
        return render(request,"model_form/userWishlist_form.html",{'form':obj})
    # @login_required
    def post(self,request):
        obj=UserWishlistForm(request.POST,request.FILES)
        if obj.is_valid():
            instance=obj.save()
            print(instance.banner_path.path)
            return redirect('customAdminPanel:userWishlist')
        else:
            return render(request,"model_form/userWishlist_form.html",{'form':obj})

@login_required(redirect_field_name='login', login_url='/adminpanel/login')
def userWishlist_check(request): 
    fm = UserWishList.objects.all() 
    context = {'form':fm}
    return render(request,"userWishlist.html",context)