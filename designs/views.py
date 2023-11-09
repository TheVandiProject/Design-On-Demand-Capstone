from fileinput import filename
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


def main_page_view(request):
    return render(request, 'designs/main_page.html')

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

def upload_design_view(request):
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["image"]
            
            # Create a path for the image
            img = Image.open(file)
            file_path = "media/uploaded/" + file.name
            print(file_path)
            img.save(file_path)
            result = handle_uploaded_image(img, file_path)
            if result is True:
                return redirect('user_home')
        else:
            return HttpResponse("Error uploading design")
    else:
        form = UploadDesignForm()
    return render(request, 'designs/user_home.html', {'form': form})

# media_storage = 'designs/images/media'

def handle_uploaded_image(image, path):
    if image is None:
        return "No image was uploaded"
    
    try:
        with open(path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return True  # Success
    except Exception as e:
        # Handle any exceptions or errors that may occur
        print(f"Error handling the uploaded image: {e}")
        return str(e)  # Return the error message
    # try:
    #     img = Image.open(image)
    #     # Get the format of the image
    #     img_format = img.format

    #     # Ensure the image is in RGB mode (for common image formats)
    #     img = img.convert('RGB')

    #     # Check the image format and save accordingly (PNG or JPEG)
    #     if img_format == "PNG":
    #         img.save(path, "PNG")
    #     elif img_format == "JPEG" or img_format == "JPG":
    #         img.save(path, "JPEG")
    #     else:
    #         img.close()
    #         return "Unsupported image format"  # Handle unsupported formats

    #     # Close the image
    #     img.close()
        
    #     classification_results = classify_image(path)
        
    #     return classification_results
    # except Exception as e:
    #     # Handle any exceptions or errors that may occur
    #     print(f"Error handling the uploaded image: {e}")
    #     return False  # Return False to indicate an error