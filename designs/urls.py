from django.urls import path
from . import views
from designs import image_label, views
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

# app_name = "designs"

urlpatterns = [
    #path("", views.index, name="index"),
    path('', views.main_page_view, name='designs'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.user_home_view, name='user_home'),
    path('logout/', views.logout_view, name='logout'),
    path('home/upload/', views.upload_design_view, name="upload_design"),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
