from django.urls import path
from designs import views
from django.conf import settings
from django.conf.urls.static import static

# app_name = "designs"

urlpatterns = [
    # path("", views.index, name="index"),
    path('', views.main_page_view, name='designs'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.render_home_view, name='user_home'),
    path('logout/', views.logout_view, name='logout'),
    path('home/upload/', views.upload_design_view, name="upload_design"),
    path('aboutus/', views.aboutus_view, name='about_us'),
    path('privacypolicy/', views.privacypolicy_view, name='privacy_policy'),
    path('index/', views.index_view, name='index'),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
