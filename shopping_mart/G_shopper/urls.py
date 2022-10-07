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
    path('delete-from-cart',views.delete_cart_item,name='delete-from-cart'),
    path('update-cart',views.update_cart_item,name='update-cart'),
    ]