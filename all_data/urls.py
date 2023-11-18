from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_list, name='users_list'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
]