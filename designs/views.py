# from fileinput import filename
# from django.core.files.base import ContentFile
import os
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, UploadDesignForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
# from .models import UploadDesign
from designs.forms import UploadDesignForm
# from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image # Pillow library for image resizing
from .image_label import classify_image
# from django.db import models
from .models import ImageUpload


def main_page_view(request):
    return render(request, 'designs/main_page.html')


def index_view(request):
    return render(request, 'designs/index.html')


def render_home_view(request):
    if(request.user.is_authenticated):
        return render(request, 'designs/user_home.html')
    else:
        return render(request, 'designs/NonUser_Home.html')


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
    return redirect("/") 


# def get_random_images(label, num_images=10):
#     try:
#         base_path = os.path.join(settings.STATIC_ROOT, 'designs', 'images')
#         if not os.path.exists(base_path):
#             return f"The directory {base_path} does not exist."

#         images = [os.path.join('designs', 'images', label, img)
#                  for img in os.listdir(base_path)
#                  if os.path.isfile(os.path.join(base_path, img))]

#         if not images:
#             return "The directory is empty."

#         return random.sample(images, min(num_images, len(images)))
#     except Exception as e:
#         return str(e)


# def swiper_view(request):
#     if request.user.is_authenticated:
#         template_name = 'designs/user_home.html'
#     else:
#         template_name = 'designs/NonUser_Home.html'
#     # Call the classify_image function to get predictions
#     classification_result = classify_image(request)
    
#     top_prediction_images = get_random_images(classification_result["top_predictions"])
    
#     other_prediction_images = {}
#     for prediction in classification_result["other_predictions"]:
#         label = prediction["label"]
#         images = get_random_images(label)
#         other_prediction_images[label] = images

#     return render(request, template_name, {'top_prediction_images': top_prediction_images, 'other_prediction_images': other_prediction_images})

def get_file_names(label):
    folder_path = os.path.join('static', 'designs', 'images', label.lower())
    
    try:
        files = os.listdir(folder_path)
        return files
    except FileNotFoundError:
        # Handle the case where the folder doesn't exist
        return []

def upload_design_view(request):
    form = UploadDesignForm()
    if request.user.is_authenticated:
        template_name = 'designs/user_home.html'
    else:
        template_name = 'designs/NonUser_Home.html'
    
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        
        if not request.FILES.get('image'):
            form.errors['image'] = 'Please select an image to upload.'
            return render(request, template_name, {'form': form})
            
        if form.is_valid():
            # file = request.FILES["image"]
            file = ImageUpload(image = request.FILES['image'])  
            file.save()
            
            # uploaded_image_url = f"/{file_path[6:]}"
            uploaded_image_url = f"{file.image.url}"
            classification_result = classify_image(request)
            top_prediction_images = get_file_names(classification_result["top_predictions"])
    
            other_prediction_images = {}
            for prediction in classification_result["other_predictions"]:
                label = prediction["label"]
                images = get_file_names(label)
                other_prediction_images[label] = images
            
            context = {
                'form': form,
                'classification_result': classification_result,
                'uploaded_image_url': uploaded_image_url,
                'top_prediction_images': top_prediction_images,
                'other_prediction_images': other_prediction_images
            }
            return render(request, template_name, context)
        else:
            return HttpResponse("Error uploading image")
        
    return render(request, template_name, {'form': form})