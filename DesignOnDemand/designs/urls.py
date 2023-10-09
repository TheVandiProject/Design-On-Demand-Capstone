from django.urls import path
from . import views

# app_name = "designs"

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.user_home_view, name='user_home'),
    path('logout/', views.logout_view, name='logout'),
]
