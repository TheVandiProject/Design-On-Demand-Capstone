from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UploadDesignForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse
# # from .models import UploadDesign
from designs.forms import *
# # from django.core.files.storage import FileSystemStorage
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

def user_settings_view(request):
    return render(request, 'designs/user_settings.html')

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
            
            uploaded_image_url = f"{file.image.url}"
            classification_result = classify_image(request)
            
            context = {
                'form': form,
                'classification_result': classification_result,
                'uploaded_image_url': uploaded_image_url,
            }
            return render(request, template_name, context)
        else:
            return HttpResponse("Error uploading image")
        
    return render(request, template_name, {'form': form})
    
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user=form.save()
            #add if statement in html to print success message
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!', extra_tags='success')
            return redirect('/designs/user_settings')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags='error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'designs/user_settings.html', {'form': form})

@login_required
def update_profile(request):
    
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return HttpResponse("invalid user_profile!")
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_settings') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'designs/user_settings.html', context)

        