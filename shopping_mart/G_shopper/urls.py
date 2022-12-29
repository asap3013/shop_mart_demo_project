from django.urls import path 
from G_shopper import views
from .views import  PasswordsChangeView
from django.contrib.auth import views as auth_views



app_name = 'G_shopper'

urlpatterns = [
    path('login/', views.userLogin, name='login'),
    # path('',views.base_page,name='base'),
    path('home/',views.home_page,name='home'),
    # path('load-more-data',views.load_more_data,name='load_more_data'),
    path('loggedout/',views.logoutuser,name='loggedout'),
    path('registration/',views.UserRegister.as_view(),name='register'),
    path('mycart/',views.add_cart,name='cart'),
    path('cart/',views.cart_list,name='addcart'),
    path('deletefromcart/',views.delete_cart_item,name='delete-from-cart'),
    path('updatecart/',views.update_cart_item,name='update-cart'),
    path('add-wishlist/',views.add_wishlist, name='add_wishlist'),
    path('my-wishlist/',views.my_wishlist, name='my_wishlist'),
    path("delete/",views.DeleteWishlist.as_view(),name="DeleteWishlist"),
    path('product/<int:product_id>',views.product_detail, name='product_detail'),
    path('coupon/',views.couponcalculate, name='couponcal'),
    path('checkout/',views.checkout,name='checkout'),
    path('address/',views.Add_address.as_view(),name='address'),    
    path('placeorder/',views.placeorder,name='placeorder'),
    path('stripe/',views.stripe_order,name='stripe'),
    path('cod/',views.cashondelivery,name='cod'),
    path('category/',views.category_filter,name='category'),
    path('price/',views.price_filter,name='price'),
    path('order_track/',views.tracking_order,name='order_track'),
    path('contact/',views.contact_us,name='contact'),
    path('my_order/',views.my_order,name='my_order'),
    path('my_account/',views.my_account,name='my_account'),
    path('edit-profile/',views.edit_profile, name='edit-profile'),
    path('password/',PasswordsChangeView.as_view(template_name='changepassword.html'),name='password'),
    path('password_success',views.password_success,name='password_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete')
    ]