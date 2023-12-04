from django.urls import path
from . import views

urlpatterns = [
    #path('users/', views.users_list, name='users_list'),
    path('users/', views.user_change_email, name='users_detail'),
    #path('user/login/', views.register_new_user, name)
]