from os import stat
from django.urls import path 
from customAdminPanel import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'customAdminPanel'

urlpatterns = [
    path('login/', views.adminLogin, name='admin_login'),
    path('',views.index,name='index'),
    path('logout/',views.logoutUser,name='logoutuser'),
    path('banner/',views.banner_check, name='banner'),
    path('banner_form/',views.Banner_field.as_view(),name='banner_form')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)