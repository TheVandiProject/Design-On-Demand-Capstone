from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from designs.forms import *
from django.contrib import messages
from rest_framework import status
from .models import Users
from .serializers import UsersSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def users_list(request):
    """
    List all books or create a new book
    """
    if request.method == 'GET':
        books = Users.objects.all()
        serializer = UsersSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def register_new_user(request):
    if request.method == 'POST':

        serializer = UsersSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, f"Account created successfully!", extra_tags='success')
            return redirect('user_home') 
    
    return render(request, 'designs/sign_up.html')

@api_view(['GET', 'PUT', 'DELETE'])
def users_detail(request, pk):
    """
    Retrieve, update or delete a book
    """
    try:
        book = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UsersSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UsersSerializer(book, data=request.data)

@api_view(['GET', 'POST'])
def user_login_view(request):

    if request.method == 'POST':
        user = request.data['username']
        passw = request.data['password']
        books = Users.objects.all().filter(username=user).filter(password=passw)
        if len(books) == 0:
            return render(request, 'designs/login_page.html')
        else:
            return redirect('user_home') 
   
    return render(request, 'designs/login_page.html')