# from fileinput import filename
# from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
# from .models import UploadDesign
from designs.forms import UploadDesignForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image # Pillow library for image resizing
from .image_label import classify_image
from datetime import datetime
from django.db import models


def main_page_view(request):
    return render(request, 'designs/main_page.html')

def index_view(request):
    return render(request, 'designs/index.html')

def user_home_view(request):
    return render(request, 'designs/user_home.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.", extra_tags='success')
                return redirect('user_home') #TODO change later to the user home page
            else:
                messages.error(request,"Invalid username or password.", extra_tags='error')
                # form.add_error(None, "Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.", extra_tags='error')
            # form.add_error(None, "Invalid username or password.")
    form = AuthenticationForm()    
    return render(request, 'designs/login_page.html', {'login_form': form})

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully!", extra_tags='success')
            return redirect('user_home') #TODO change later to the user home page       
        # form.add_error(None, "Unsuccessful registration. Invalid information.")
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.", extra_tags='error')
        form = RegisterForm()
      
    return render(request, 'designs/sign_up.html', {'signin_form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.", extra_tags='success')
    return redirect("/designs/") 

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploaded/')

def upload_design_view(request):
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        if form.is_valid():
            # file = request.FILES["image"]
            file = ImageUpload(image = request.FILES['image'])
            
            # Create a path for the image
            # img = Image.open(file).convert('RGB')
            # file_path = "media/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" +  file.name
            # img.save(file_path)
            file.save()
            
            # uploaded_image_url = f"/{file_path[6:]}"
            uploaded_image_url = f"{file.image.url}"
            classification_result = classify_image(request)
            return render(request, 'designs/user_home.html', {'form': form, 'classification_result': classification_result, 'uploaded_image_url': uploaded_image_url})
        else:
            return HttpResponse("Error uploading image")
    else:
        form = UploadDesignForm()
    return render(request, 'designs/user_home.html', {'form': form})