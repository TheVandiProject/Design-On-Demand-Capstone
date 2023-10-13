from django.urls import path
from . import views
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

# app_name = "designs"

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.user_home_view, name='user_home'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_design_view, name="upload_design"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
