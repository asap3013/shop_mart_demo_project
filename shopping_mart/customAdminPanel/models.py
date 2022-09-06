import email
from django.contrib.auth.models import Group
from email import message
from email.policy import default
from itertools import product
from unicodedata import category, decimal, name
from django.db import models

class Configuration(models.Model):
    conf_key = models.CharField(max_length=45)
    conf_value = models.CharField(max_length=100)
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)
    modify_status = models.BooleanField()

    def __str__(self):
        return self.Configuration

    class Meta:
        verbose_name = "Configuration"
        verbose_name_plural = "Configuration"
   

class Cms(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    meta_title = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.CmsTitle

    class Meta:
        verbose_name = "Cms"
        verbose_name_plural = "Cms" 

class Banners(models.Model):
    banner_name = models.CharField(max_length=50 , unique=True)
    banner_path = models.ImageField(upload_to='shop_mart/images',default="")
    status = models.BooleanField()


    class Meta:
        db_table = "customAdminPanel_banners"
        verbose_name = "Banners"
        verbose_name_plural = "Banners" 




class EmailTemplate(models.Model):
    title = models.CharField(max_length=45)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.EmailTemplate
    
    class Meta:
        verbose_name = "EmailTemplate"
        verbose_name_plural = "EmailTemplate"

class ContactUs(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    contact_no = models.CharField(max_length=45)
    message = models.TextField()
    note_admin = models.TextField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ContactUs

    class Meta:
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.IntegerField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField()

    def __str__(self):
        return self.Category

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=45)
    short_description = models.CharField(max_length=100)
    long_description = models.TextField()
    price = models.FloatField()
    special_price_from = models.DateTimeField()
    special_price_to = models.DateTimeField()
    status = models.BooleanField()
    quantity = models.IntegerField()
    meta_title = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField()

    def __str__(self):
        return self.Product

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product" 


class ProductCategories(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.ProductCategories

    class Meta:
        verbose_name = "ProductCategories"
        verbose_name_plural = "ProductCategories"

class ProductImages(models.Model):
    image_name = models.CharField(max_length=100)
    status = models.BooleanField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True)   
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.ProductImages

    class Meta:
        verbose_name = "ProductImages"
        verbose_name_plural = "ProductImages"


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_date = models.DateTimeField(auto_now_add=True)
    # to_token = models.CharField(max_length=100)
    # twitter_token = models.CharField(max_length=100)
    # google_token = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_group')
    specify_role = [('M','manager'),('C','customer'),('A','admin')]
    role = models.CharField(max_length=10, choices=specify_role,default='')
    
    # def __str__(self):
    #     return self.User

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"



class UserWishList(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.IntegerField()

    def __str__(self):
        return self.UserWishList

    class Meta:
        verbose_name = "UserWishList"
        verbose_name_plural = "UserWishList"


class UserAddress(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    zip_code = models.CharField(max_length=45)

    def __str__(self):
        return self.UserAddress

    class Meta:
        verbose_name = "UserAddress"
        verbose_name_plural = "UserAddress"


class Coupon(models.Model):
    code = models.CharField(max_length=45)
    percent_off = models.FloatField()
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True) 
    no_of_user = models.IntegerField()

    def __str__(self):
        return self.Coupon

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupon"  


class CouponsUsed(models.Model):
    user_id = models.IntegerField() 
    order_id = models.IntegerField() 
    created_date = models.DateField()
    coupon_id = models.ForeignKey(Coupon,on_delete=models.CASCADE)

    def __str__(self):
        return self.UsedCoupons

    class Meta:
        verbose_name = "UsedCoupons"
        verbose_name_plural = "UsedCoupons"



class PaymentGateway(models.Model):
    name = models.CharField(max_length=45)
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.PaymentGateway

    class Meta:
        verbose_name = "PaymentGateway"
        verbose_name_plural = "PaymentGateway"  



class ProductAttributes(models.Model):
    name = models.CharField(max_length=45)
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return self.ProductAttributesName

    class Meta:
        verbose_name = "ProductAttributes"
        verbose_name_plural = "ProductAttributes"



class ProductAttributesValues(models.Model):
    product_attribute_id = models.ForeignKey(ProductAttributes,on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=45)
    created_by = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.ProductAttributesValues

    class Meta:
        verbose_name = "ProductAttributesValues"
        verbose_name_plural = "ProductAttributesValues"


class ProductAttributesAssoc(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_attribute_id = models.ForeignKey(ProductAttributes,on_delete=models.CASCADE)
    product_attribute_value = models.ForeignKey('ProductAttributesAssoc',on_delete=models.CASCADE)

    def __str__(self):
        return self.ProductAttributesAssoc

    class Meta:
        verbose_name = "ProductAttributesAssoc"
        verbose_name_plural = "ProductAttributesAssoc"


class OrderDetails(models.Model):
    order_id = models.IntegerField()
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.FloatField()

    def __str__(self):
        return self.OrderDetails

    class Meta:
        verbose_name = "OrderDetails"
        verbose_name_plural = "OrderDetails"


class userOrder(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_method = models.IntegerField()
    AWB_NO =models.CharField(max_length=100)
    payment_gateway = models.ForeignKey(PaymentGateway,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    grand_total = models.FloatField()
    shipping_charges = models.FloatField()
    coupon_id = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    billing_address_1 = models.CharField(max_length=100)
    billing_address_2 = models.CharField(max_length=100)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    billing_zipcode = models.CharField(max_length=100)
    shipping_address_1 = models.CharField(max_length=100)
    shipping_address_2 = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=100)
    shipping_zipcode = models.CharField(max_length=100)

    def __str__(self):
        return self.UserOrder

    class Meta:
        verbose_name = "userOrder"
        verbose_name_plural = "userOrder"




