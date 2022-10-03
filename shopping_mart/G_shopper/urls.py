from django.urls import path 
from G_shopper import views

app_name = 'G_shopper'

urlpatterns = [
    # path('loggin/', views.login, name='login'),
    path('userlogin/', views.userLogin, name='user_login'),
    path('',views.base_page,name='base'),
    path('registration/',views.UserRegister.as_view(),name='register')
    ]