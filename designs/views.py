from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
# from .models import UploadDesign
from designs.forms import *
# from django.core.files.storage import FileSystemStorage
from PIL import Image # Pillow library for image resizing


def main_page_view(request):
    return render(request, 'designs/main_page.html')

def index_view(request):
    return render(request, 'designs/index.html')

def user_home_view(request):
    return render(request, 'designs/user_home.html')

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
                return redirect('/home/') #TODO change later to the user home page
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
            return redirect('/designs/user_home') #TODO change later to the user home page       
        messages.error(request, "Unsuccessful registration. Invalid information.", extra_tags='error')
        # form.add_error(None, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()   
    return render(request, 'designs/sign_up.html', {'signin_form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.", extra_tags='success')
    return redirect("/designs/") 

@login_required(login_url='/designs/login/')
def upload_design_view(request):
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES["image"]
            file_path = "designs/images/media"  # Specify your file path with the desired format
            result = handle_uploaded_image(uploaded_image, file_path)
            if result is True:
                return HttpResponseRedirect('/designs/home')
        else:
            return HttpResponse("Error uploading design")
    else:
        form = UploadDesignForm()
    return render(request, 'designs/user_home.html', {'form': form})

media_storage = 'designs/images/media'

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
def profile(request):
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

        