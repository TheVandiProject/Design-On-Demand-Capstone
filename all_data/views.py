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
def register_new_user(request):
    if request.method == 'POST':

        serializer = UsersSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, f"Account created successfully!", extra_tags='success')
            return redirect('user_home') 
    
    return render(request, 'designs/sign_up.html')

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

@api_view(['GET', 'POST', 'PUT'])
def user_change_email(request):
    if request.method == 'GET':
        books = Users.objects.all()
        serializer = UsersSerializer(books, many=True)
        return Response(serializer.data)

    if request.method == 'PUT':
        old_email_address = request.data['old_email_address']
        new_email_address = request.data['new_email_address']
        books = Users.objects.all().filter(email_address=old_email_address).update(email_address=new_email_address)
        print(old_email_address)
        print(new_email_address)
        #print(books[1])
        #books = new_email_address
        # serializer = UsersSerializer(books)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if len(books) == 0:
        #     return render(request, 'designs/login_page.html')
        # else:
        #     return redirect('user_home') 

@api_view(['GET', 'POST'])
def update_profile(request):
    
    if request.method == 'POST':

        if 'update_email' in request.POST:
            new_email_address = request.data['new_email_address']
            old_email_address = request.data['old_email_address']
            Users.objects.all().filter(email_address=old_email_address).update(email_address=new_email_address)
            messages.success(request, 'Your email has been updated!')

        if 'update_username' in request.POST:
            new_username = request.data['new_username']
            old_username = request.data['old_username']
            Users.objects.all().filter(username=old_username).update(username=new_username)
            messages.success(request, 'Your username has been updated!')        

        # if not new_username and not new_email_address:
        #     messages.error(request, 'Please enter a valid username or email.')

        if 'update_password' in request.POST:
            this_email_address = request.data['email_address']
            this_username = request.data['username']
            old_password = request.data['old_password']
            new_password = request.data['new_password']
            Users.objects.all().filter(email_address=this_email_address).filter(username=this_username).filter(password=old_password).update(password=new_password)

        return redirect('user_home')
        #return print()#redirect('user_settings')
    

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'designs/user_settings.html', {'form': form})

