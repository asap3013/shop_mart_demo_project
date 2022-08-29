from unicodedata import category
from django.contrib import admin
from customAdminPanel.models import *

# Register your models here.
class ConfigurationAdmin(admin.ModelAdmin):
    list_display=('conf_key','conf_value','created_by','created_date','modify_by','modify_date','modify_status')
admin.site.register(Configuration,ConfigurationAdmin)


class CmsAdmin(admin.ModelAdmin):
    list_display=('title','content','meta_title','meta_description','meta_keywords','created_by','created_date','modify_by','modify_date')
admin.site.register(Cms,CmsAdmin)

class BannersAdmin(admin.ModelAdmin):
    list_display =('banner_path','status')
admin.site.register(Banners,BannersAdmin)


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display=('title','subject','content','created_by','created_date','modify_by','modify_date')
admin.site.register(EmailTemplate,EmailTemplateAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display=('name','email','contact_no','message','note_admin','created_by','created_date','modify_by','modify_date')
admin.site.register(ContactUs,ContactUsAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','parent_id','created_by','created_date','modify_by','modify_date','status')
admin.site.register(Category,CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','sku','short_description','long_description','price','special_price_from','special_price_to','status','quantity','meta_title','meta_description','meta_keywords','created_by','created_date','modify_by','modify_date','is_featured')
admin.site.register(Product,ProductAdmin)


class ProductCategoriesAdmin(admin.ModelAdmin):
    list_display = ('product_id','category_id')
admin.site.register(ProductCategories,ProductCategoriesAdmin)


class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('image_name','status','created_by','created_date','modify_by','modify_date','product_id')
admin.site.register(ProductImages,ProductImagesAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','password','created_date','role')
admin.site.register(User,UserAdmin)


class UserWishlistAdmin(admin.ModelAdmin):
    list_display = ('user_id','product_id')
admin.site.register(UserWishList,UserWishlistAdmin)

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user_id','address_1','address_2','city','state','country','zip_code')
admin.site.register(UserAddress,UserAddressAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_dislay = ('code','percent_off','created_by','created_date','modify_by','modify_date','no_of_user')
admin.site.register(Coupon,CouponAdmin)


class CouponsUsedByAdmin(admin.ModelAdmin):
    list_display = ('user_id','order_id','created_date','coupon_id')
admin.site.register(CouponsUsed,CouponsUsedByAdmin)


class PaymentGatewayAdmin(admin.ModelAdmin):
    list_dislay = ('name','created_by','created_date','modify_by','modify_date')
admin.site.register(PaymentGateway,PaymentGatewayAdmin)


class ProductAttributesAdmin(admin.ModelAdmin):
    list_display = ('name','created_by','created_date','modify_by','modify_date')
admin.site.register(ProductAttributes,ProductAttributesAdmin)


class ProductAttributesValuesAdmin(admin.ModelAdmin):
    list_display = ('product_attribute_id','attribute_value','created_by','created_date','modify_by','modify_date')
admin.site.register(ProductAttributesValues,ProductAttributesValuesAdmin)

class ProductAttributesAssocAdmin(admin.ModelAdmin):
    list_display = ('product_id','product_attribute_id','product_attribute_value')
admin.site.register(ProductAttributesAssoc,ProductAttributesAssocAdmin)

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_id','product_id','quantity','amount')
admin.site.register(OrderDetails,OrderDetailsAdmin)


class userOrderAdmin(admin.ModelAdmin):
    list_display = ('user_id','shipping_method','AWB_NO','payment_gateway','transaction_id','created_date','status','grand_total','shipping_charges','coupon_id','billing_address_1','billing_address_2','billing_city','billing_state','billing_country','billing_zipcode','shipping_address_1','shipping_address_2','shipping_city','shipping_state','shipping_country','shipping_zipcode')
admin.site.register(userOrder,userOrderAdmin)