from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import UploadDesign
from designs.forms import UploadDesignForm
from django.core.files.storage import FileSystemStorage
from PIL import Image # Pillow library for image resizing



def index(request):
    return render(request, 'index.html')

def user_home_view(request):
    return render(request, 'public/user_home.html')

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
                return redirect('/public/home') #TODO change later to the user home page
            else:
                messages.error(request,"Invalid username or password.", extra_tags='error')
                # form.add_error(None, "Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.", extra_tags='error')
            # form.add_error(None, "Invalid username or password.")
    form = AuthenticationForm()    
    return render(request, 'public/login_page.html', {'login_form': form})

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully!", extra_tags='success')
            return redirect('/public/home') #TODO change later to the user home page       
        messages.error(request, "Unsuccessful registration. Invalid information.", extra_tags='error')
        # form.add_error(None, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()   
    return render(request, 'public/sign_up.html', {'signin_form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.", extra_tags='success')
    return redirect("/public/") 

def upload_design_view(request):
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES["image"]
            file_path = "designs/static/designs/images/media"  # Specify your file path with the desired format
            result = handle_uploaded_image(uploaded_image, file_path)
            if result is True:
                return HttpResponseRedirect('/public/home')
        else:
            return HttpResponse("Error uploading design")
    else:
        form = UploadDesignForm()
    return render(request, 'public/user_home.html', {'form': form})

media_storage = 'designs/static/designs/images/media'

def handle_uploaded_image(image, path):
    try:
        img = Image.open(image)
        # Ensure the image is in RGB mode (for common image formats)
        img = img.convert('RGB')

        # Check the image format and save accordingly (PNG or JPEG)
        if img.format == "PNG":
            img.save(path, "PNG")
        elif img.format == "JPEG":
            img.save(path, "JPEG")
        else:
            return "Unsupported image format"  # Handle unsupported formats

        # Close the image
        img.close()

        return True  # Success
    except Exception as e:
        # Handle any exceptions or errors that may occur
        print(f"Error handling the uploaded image: {e}")
        return False  # Return False to indicate an error