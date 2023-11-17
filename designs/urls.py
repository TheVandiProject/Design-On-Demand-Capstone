from django.urls import path
from . import views
from designs import views
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

# app_name = "designs"

urlpatterns = [
    #path("", views.index, name="index"),
    path('', views.main_page_view, name='designs'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.user_home_view, name='user_home'),
    path('home/upload/', views.upload_design_view, name="upload_design"),
    path('home/settings/', views.user_settings_view, name='user_settings'),
    path('home/settings/password-change/', views.change_password, name='change_password'),
    path('home/settings/profile/', views.profile, name='profile'),
    path('index/', views.index_view, name='index'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
