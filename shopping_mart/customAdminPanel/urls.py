from os import stat
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
    path("edit/<int:id>" ,views.EditBanner.as_view(),name="Edit")
]



