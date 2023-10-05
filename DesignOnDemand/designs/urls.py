from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup')
]
