from django.urls import path 
from customAdminPanel import views

app_name = 'customAdminPanel'

urlpatterns = [
    path('login/', views.adminLogin, name='admin_login'),
    path('',views.index,name='index'),
    path('logout/',views.logoutUser,name='logoutuser')
]