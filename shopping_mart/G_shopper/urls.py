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
    # path('cart/<int:product_id>/', views.add_to_cart, name='add'),
    # path('cart/', views.get_cart, name='cart'),

    ]