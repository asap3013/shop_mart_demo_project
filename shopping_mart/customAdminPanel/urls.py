from os import stat
from unicodedata import category
from django.urls import path 
from customAdminPanel import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required 

app_name = 'customAdminPanel'

urlpatterns = [
    path('login/', views.adminLogin, name='admin_login'),
    path('',views.index,name='index'),
    path('logout/',views.logoutUser,name='logoutuser'),
    path('banner/',views.banner_check, name='banner'),
    path('banner_form/',views.BannerField.as_view(),name='banner_form'),
    path("delete/",views.DeleteBanner.as_view(),name="Delete"),
    path("edit/<int:id>" ,views.EditBanner.as_view(),name="Edit"),
    path('category/',views.category_check, name='category'),
    path('category_form',views.CategoryField.as_view(),name='category_form'),
    path("Delete_category/",views.DeleteCategory.as_view(),name="Delete_category"),
    path("editCategory/<int:id>" ,views.EditCategory.as_view(),name="EditCategory"),
    path('cms/',views.cms_check, name='cms'),
    path('cms_form/',views.CmsField.as_view(),name='cms_form'),
    path("Delete_cms/",views.DeleteCms.as_view(),name="Delete_cms"),
    path("editCms/<int:id>" ,views.EditCms.as_view(),name="EditCms"),
    path('configuration/',views.configuration_check, name='configuration'),
    path('configuration_form/',views.ConfigurationField.as_view(),name='configuration_form'),
    path('contactUs/',views.contactUs_check, name='contactUs'),
    path('contactUs_form/',views.ContactUsField.as_view(),name='contactUs_form'),
    path('coupon/',views.coupon_check, name='coupon'),
    path('coupon_form/',views.CouponField.as_view(),name='coupon_form'),
    path("coupondelete/",views.DeleteCoupon.as_view(),name="Delete_coupon"),
    path("editCoupon/<int:id>" ,views.EditCoupon.as_view(),name="EditCoupon"),
    path('email/',views.email_check, name='email'),
    path('email_form/',views.EmailField.as_view(),name='email_form'),
    path('emaildelete/',views.DeleteEmail.as_view(),name='emaildelete'),
    path("editEmail/<int:id>" ,views.EditEmail.as_view(),name="EditEmail"),
    path('orderDetail/',views.orderDetail_check, name='orderDetail'),
    path('orderDetail_form/',views.OrderDetailField.as_view(),name='orderDetail_form'),
    path('detail_order/<int:order_id>',views.detail_order.as_view(),name='detail_order'),
    path('paymentGateway/',views.paymentGateway_check, name='paymentGateway'),
    path('paymentGateway_form/',views.PaymentGatewayField.as_view(),name='paymentGateway_form'),
    path('product/',views.product_check, name='product'),
    path('product_form/',views.ProductField.as_view(),name='product_form'),
    path("productdelete/",views.DeleteProduct.as_view(),name="Delete_product"),
    path("editProduct/<int:id>" ,views.EditProduct.as_view(),name="EditProduct"),
    path('productAttributes/',views.productAttributes_check, name='productAttributes'),
    path('productAttributes_form/',views.ProductAttributesField.as_view(),name='productAttributes_form'),
    path("productAttributesdelete/",views.DeleteProductAttributes.as_view(),name="Delete_productAttributes"),
    path("editProductAttributes/<int:id>" ,views.EditProductAttributes.as_view(),name="EditProductAttributes"),
    path('productAttributesAssoc/',views.productAttributesAssoc_check, name='productAttributesAssoc'),
    path('productAttributesAssoc_form/',views.ProductAttributesAssocField.as_view(),
    name='productAttributesAssoc_form'),
    path('ajax/productAttributesValue/',views.getAttributeValues, name='productAttributesValue'),
    path('productAttributesValues/',views.productAttributesValues_check, name='productAttributesValues'),
    path('productAttributesValues_form/',views.ProductAttributesValuesField.as_view(),name='productAttributesValues_form'),
    path('productCategory/',views.productCategory_check, name='productCategory'),
    path('productCategory_form/',views.ProductCategoryField.as_view(),name='productCategory_form'),
    path("productCategorydelete/",views.DeleteProductCategory.as_view(),name="Delete_productCategory"),
    path("editProductCategory/<int:id>" ,views.EditProductCategory.as_view(),name="EditProductCategory"),
    path('productImages/',views.productImages_check, name='productImages'),
    path('productImages_form/',views.ProductImagesField.as_view(),name='productImages_form'),
    path("productImagesdelete/",views.DeleteProductImage.as_view(),name="Delete_productImage"),
    path("editProductImage/<int:id>" ,views.EditProductImage.as_view(),name="EditProductImage"),
    path('usedCoupon/',views.usedCoupon_check, name='usedCoupon'),
    path('usedCoupon_form/',views.UsedCouponField.as_view(),name='usedCoupon_form'),
    path('user/',views.user_check, name='user'),
    path('user_form/',views.UserField.as_view(),name='user_form'),
    path('userAddress/',views.userAddress_check, name='userAddress'),
    path('userAddress_form/',views.UserAddressField.as_view(),name='userAddress_form'),
    path('userOrder/',views.userOrder_check, name='userOrder'),
    path('userOrder_form/',views.UserOrderField.as_view(),name='userOrder_form'),
    path("userOrderdelete/",views.DeleteUserOrder.as_view(),name="Delete_userOrder"),
    path("edituserOrder/<int:id>" ,views.EditUserOrder.as_view(),name="Edit_userOrder"),
    path('userWishlist/',views.userWishlist_check, name='userWishlist'),
    path('userWishlist_form/',views.UserWishlistField.as_view(),name='userWishlist_form'),
    path("userWishlistdelete/",views.DeleteuserWishlist.as_view(),name="Delete_userWishlist"),
    

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)




