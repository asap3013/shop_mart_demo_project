from django import forms  
from customAdminPanel.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# class UserForm(forms.ModelForm):  
#     class Meta:  
#         model = User
#         fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email")

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "email")

class BannersForm(forms.ModelForm):  
    class Meta:  
        model = Banners  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class CategoryForm(forms.ModelForm):  
    class Meta:  
        model = Category  
        fields = '__all__'

class CmsForm(forms.ModelForm):  
    class Meta:  
        model = Cms  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class ConfigurationForm(forms.ModelForm):  
    class Meta:  
        model = Configuration  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

        
class EmailTemplateForm(forms.ModelForm):  
    class Meta:  
        model = EmailTemplate  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class OrderDetailsForm(forms.ModelForm):  
    class Meta:  
        model = OrderDetails  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class PaymentGatewayForm(forms.ModelForm):  
    class Meta:  
        model = PaymentGateway  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class ContactUsForm(forms.ModelForm):  
    class Meta:  
        model = ContactUs  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

class CouponForm(forms.ModelForm):  
    class Meta:  
        model = Coupon  
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class ProductForm(forms.ModelForm):  
    class Meta:  
        model = Product 
        fields = ['name','sku','short_description','long_description','price','status','quantity','meta_title','meta_description','meta_keywords','is_featured']
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

class ProductAttributesForm(forms.ModelForm):  
    class Meta:  
        model = ProductAttributes
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')


class ProductAttributesAssocForm(forms.ModelForm):  
    class Meta:  
        model = ProductAttributesAssoc
        fields = ['product_attribute_id','product_attribute_value']
    

class ProductAttributesValuesForm(forms.ModelForm):  
    class Meta:  
        model = ProductAttributesValues
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_attribute_value'].queryset = ProductAttributesValues.objects.none()

        if 'product_attribute_id' in self.data:
            try:
                product_attribute_id_id = int(self.data.get('product_attribute_id'))
                self.fields['product_attribute_value'].queryset = ProductAttributesValues.objects.filter(product_attribute_id_id=product_attribute_id_id).order_by('name')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['product_attribute_value'].queryset = self.instance.product_attribute_id.product_attribute_value.order_by('name')


class ProductCategoryForm(forms.ModelForm):  
    class Meta:  
        model = ProductCategories 
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

class ProductImagesForm(forms.ModelForm):  
    class Meta:  
        model = ProductImages 
        fields = ['image_path']
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')



class UsedCouponForm(forms.ModelForm):  
    class Meta:  
        model = CouponsUsed
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')




class UserAddressForm(forms.ModelForm):  
    class Meta:  
        model = UserAddress
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

class UserOrderForm(forms.ModelForm):  
    class Meta:  
        model = UserOrder
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')

class UserWishlistForm(forms.ModelForm):  
    class Meta:  
        model = UserWishList
        fields = '__all__'
        # labels = {'banner_path': "banner", "status": "status",}
        # exclude = ('banner_path','status')