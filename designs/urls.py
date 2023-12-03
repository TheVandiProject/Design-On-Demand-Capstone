from django.urls import path
from designs import views
from django.conf import settings
from django.conf.urls.static import static
from all_data import views as all_data

# app_name = "designs"

urlpatterns = [
    # path("", views.index, name="index"),
    path('', views.main_page_view, name='designs'),
    path('accounts/login/', all_data.user_login_view, name='logon'),
    path('login/', all_data.user_login_view, name='login'),
    path('signup/', all_data.register_new_user, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.render_nonuser_home_view, name='nonuser_home'),
    path('home/', views.render_user_home_view, name='user_home'),
    path('home/user-upload/', views.upload_user_content_view, name="upload_user_content"),
    path('upload/image-upload/', views.upload_nonuser_content_view, name="upload_nonuser_content"),
    path('home/settings/', views.user_settings_view, name='user_settings'),
    path('home/settings/password-change/', views.change_password, name='change_password'),
    path('home/settings/profile/', views.update_profile, name='update_profile'),
    path('home/designer-upload/', views.designer_design_upload_view, name='designer-upload'),
    path('index/', views.index_view, name='index'),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
