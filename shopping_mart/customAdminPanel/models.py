from django.contrib.auth.models import Group
from django.db import models
from django_mysql.models import EnumField
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField



class User(AbstractUser):
    phone = models.CharField(max_length=13,null = True)
    # first_name = models.CharField(max_length=45)
    # last_name = models.CharField(max_length=45)
    # email = models.CharField(max_length=45)
    # password = models.CharField(max_length=45)
    # created_date = models.DateTimeField(auto_now_add=True)
    # # to_token = models.CharField(max_length=100)
    # # twitter_token = models.CharField(max_length=100)
    # # google_token = models.CharField(max_length=100)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_group')
    # specify_role = [('M','manager'),('C','customer'),('A','admin')]
    # role = models.CharField(max_length=10, choices=specify_role,default='')
    


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

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
    content =RichTextField(blank=True,null=True)
    meta_title = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Cms_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Cms_modified_by')
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
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='EmailTemplate_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='EmailTemplate_modified_by')
    modify_date = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "EmailTemplate"
        verbose_name_plural = "EmailTemplate"

class ContactUs(models.Model):
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    contact_no = models.CharField(max_length=45)
    message = models.TextField()
    note_admin = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ContactUs_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ContactUs_modify_by')
    modify_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey("self", null=True,blank=True,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Category_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Category_modified_by')
    modify_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField()

    def __str__(self):
            return self.name
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=45)
    short_description = models.TextField()
    long_description = models.TextField()
    price = models.FloatField()
    special_price_from = models.DateTimeField(auto_now_add=True)
    special_price_to = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    quantity = models.IntegerField()
    meta_title = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Product_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Product_modified_by')
    modify_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField()
    # image = models.ImageField(upload_to='shop_mart/product_images',default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product" 


class ProductCategories(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.ProductCategories

    class Meta:
        verbose_name = "ProductCategories"
        verbose_name_plural = "ProductCategories"

class ProductImages(models.Model):
    image_path = models.ImageField(upload_to='shop_mart/product_images',default="")
    status = models.BooleanField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ProductImages_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ProductImages_modified_by')
    modify_date = models.DateTimeField(auto_now=True)   
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True)

    # def __str__(self):
    #     return self.image_path

    class Meta:
        verbose_name = "ProductImages"
        verbose_name_plural = "ProductImages"


class UserWishList(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.

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
        return self.address_1

    class Meta:
        verbose_name = "UserAddress"
        verbose_name_plural = "UserAddress"


class Coupon(models.Model):
    code = models.CharField(max_length=45)
    percent_off = models.FloatField()
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Coupon_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='Coupon_modified_by')
    modify_date = models.DateTimeField(auto_now=True) 
    no_of_user = models.IntegerField()

    def __str__(self):
        return self.code

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
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='PaymentGateway_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='PaymentGateway_modified_by')
    modify_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "PaymentGateway"
        verbose_name_plural = "PaymentGateway"  



class ProductAttributes(models.Model):
    name = models.CharField(max_length=45)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ProductAttributes_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ProductAttributes_modified_by')
    modify_date = models.DateTimeField(auto_now=True) 


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ProductAttributes"
        verbose_name_plural = "ProductAttributes"



class ProductAttributesValues(models.Model):
    product_attribute_id = models.ForeignKey(ProductAttributes,on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=45)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ProductAttributesValues_created_by')
    created_date = models.DateTimeField(auto_now_add=True)
    modify_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='ProductAttributesValues_modified_by')
    modify_date = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.attribute_value

    class Meta:
        verbose_name = "ProductAttributesValues"
        verbose_name_plural = "ProductAttributesValues"


class ProductAttributesAssoc(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    product_attribute_id=models.ForeignKey(ProductAttributes,on_delete=models.CASCADE,null=True,blank=True)
    product_attribute_value =models.ForeignKey(ProductAttributesValues,on_delete=models.CASCADE,blank=True)
    

    class Meta:
        verbose_name = "ProductAttributesAssoc"
        verbose_name_plural = "ProductAttributesAssoc"


class OrderDetails(models.Model):
    order_id = models.IntegerField()
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    amount = models.FloatField()



    class Meta:
        verbose_name = "OrderDetails"
        verbose_name_plural = "OrderDetails"


class UserOrder(models.Model):
    OUT_FOR_DELIVERY = 'Out for delivery'
    PENDING = 'pending'
    PLACED = 'Placed'

    CHOICES = (
        (OUT_FOR_DELIVERY, 'Out for delivery'),
        (PENDING, 'Pending'),
        (PLACED, 'Placed'),
    )
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    # shipping_method = models.IntegerField()
    # AWB_NO =models.CharField(max_length=100)
    payment_gateway = models.ForeignKey(PaymentGateway,null=True,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=CHOICES, default=OUT_FOR_DELIVERY)
    grand_total = models.FloatField()
    shipping_charges = models.FloatField()
    coupon_id = models.ForeignKey(Coupon,null=True,on_delete=models.CASCADE)
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
        return self.billing_address_1

    class Meta:
        verbose_name = "userOrder"
        verbose_name_plural = "userOrder"




