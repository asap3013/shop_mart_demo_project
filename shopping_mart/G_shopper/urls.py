from django.urls import path 
from G_shopper import views

app_name = 'G_shopper'

urlpatterns = [
    path('userlogin/', views.userLogin, name='user_login'),
    # path('',views.base_page,name='base'),
    path('home/',views.home_page,name='home'),
    path('loggedout/',views.logoutuser,name='loggedout'),
    path('registration/',views.UserRegister.as_view(),name='register'),
    path('mycart/',views.add_cart,name='cart'),
    path('cart/',views.cart_list,name='addcart'),
    path('deletefromcart/',views.delete_cart_item,name='delete-from-cart'),
    path('updatecart/',views.update_cart_item,name='update-cart'),
    path('add-wishlist/',views.add_wishlist, name='add_wishlist'),
    path('my-wishlist/',views.my_wishlist, name='my_wishlist'),
    path('product/<int:id>',views.product_detail, name='product_detail'),
    path('coupon/',views.couponcalculate, name='couponcal'),
    path('checkout/',views.checkout,name='checkout'),
    path('address/',views.Add_address.as_view(),name='address')

    ]