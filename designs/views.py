from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UploadDesignForm, UploadDesignForm, UploadDesignerDesignForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .image_label import classify_image, get_designer_images
from .models import *
from all_data.models import *
from django.template import RequestContext
from django.template.response import TemplateResponse


def handler404(request, exception):
    response = TemplateResponse(request,'404.html', {})
    return response

def main_page_view(request):
    return render(request, 'designs/main_page.html')


def index_view(request):
    return render(request, 'designs/index.html')


def aboutus_view(request):
    return render(request, 'designs/about_us.html')


def privacypolicy_view(request):
    return render(request, 'designs/privacy_policy.html')

def termsconditions_view(request):
    return render(request, 'designs/terms_conditions.html')

def render_user_home_view(request):
    return render(request, 'designs/user_home.html')

def render_nonuser_home_view(request):
    return render(request, 'designs/NonUser_Home.html')

# @login_required
def user_settings_view(request):
    return render(request, 'designs/user_settings.html')

# def designer_upload_view(request):
#     return render(request, 'designs/upload_design.html')



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
            return redirect('user_home')      
        # form.add_error(None, "Unsuccessful registration. Invalid information.")
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.", extra_tags='error')
        form = RegisterForm()
      
    return render(request, 'designs/sign_up.html', {'signin_form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.", extra_tags='success')
    return redirect("/") 

# NOT RELATED TO UPLOAD DESIGN PAGE
def upload_user_content(request):
    form = UploadDesignForm()
    # if request.user.is_authenticated:
    template_name = 'designs/user_home.html'
    #     redirect_name = 'user_home'
    # else:
    #     template_name = 'designs/NonUser_Home.html'
    #     redirect_name = 'nonuser_home'
    
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        
        if not request.FILES.get('image'):
            form.errors['image'] = 'Please upload an image'
            
        if form.is_valid():
            # file = request.FILES["image"]
            file = ImageUpload(image = request.FILES['image'])  
            file.save()
            image_url = file.image.url
            
            uploaded_image_url = f"{image_url}"
            classification_result = classify_image(image_url)
            
            context = {
                'form': form,
                'classification_result': classification_result,
                'uploaded_image_url': uploaded_image_url,
            }
            return render(request, template_name, context)
        else:
            form.errors['upload'] = 'Error uploading image'
        
    return render(request, template_name, {'form': form})

def upload_nonuser_content_view(request):
    form = UploadDesignForm()
    # if request.user.is_authenticated:
    # template_name = 'designs/user_home.html'
    #     redirect_name = 'user_home'
    # else:
    template_name = 'designs/NonUser_Home.html'
    #     redirect_name = 'nonuser_home'
    
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        
        if not request.FILES.get('image'):
            form.errors['image'] = 'Please upload an image'
            
        if form.is_valid():
            # file = request.FILES["image"]
            file = ImageUpload(image = request.FILES['image'])  
            file.save()
            image_url = file.image.url
            
            uploaded_image_url = f"{image_url}"
            classification_result = classify_image(image_url)
            
            context = {
                'form': form,
                'classification_result': classification_result,
                'uploaded_image_url': uploaded_image_url,
            }
            return render(request, template_name, context)
        else:
            form.errors['upload'] = 'Error uploading image'
        
    return render(request, template_name, {'form': form})

# def upload_design_view(request):
    form = UploadDesignForm()
    # if request.user.is_authenticated:
    template_name = 'designs/user_home.html'
    #     redirect_name = 'user_home'
    # else:
    #     template_name = 'designs/NonUser_Home.html'
    #     redirect_name = 'nonuser_home'
    
    if request.method == "POST":
        form = UploadDesignForm(request.POST, request.FILES)
        
        if not request.FILES.get('image'):
            form.errors['image'] = 'Please select an image to upload.'
            
        if form.is_valid():
            # file = request.FILES["image"]
            file = ImageUpload(image = request.FILES['image'])  
            file.save()
            image_url = file.image.url
            
            uploaded_image_url = f"{image_url}"
            classification_result = classify_image(image_url)
            
            context = {
                'form': form,
                'classification_result': classification_result,
                'uploaded_image_url': uploaded_image_url,
            }
            return render(request, template_name, context)
        else:
            form.errors['upload'] = 'Error uploading image'
        
    return render(request, template_name, {'form': form})

# @login_required
def designer_design_upload_view(request):
    categories = Category.objects.all()
    design_images = get_designer_images(request)
    if request.method == 'POST':
            form = UploadDesignerDesignForm(request.POST, request.FILES)
            if not request.FILES.get('image'):
                form.errors['image'] = 'Please upload an image'
            
            if form.is_valid():
                if not form.cleaned_data['categories']:
                    form.errors['categories'] = 'Please select at least one category'
            
            if form.is_valid():                    
                uploaded_image = form.save(commit=False)
                uploaded_image.save()
                form.save_m2m()  # Save the categories
                
                context={
                    'form': form, 
                    'design_images': design_images, 
                    'categories': categories,
                    'success_message': 'Your design has been uploaded!',
                }
                
                return render(request, 'designs/upload_design.html', context) 
    else:
        form = UploadDesignerDesignForm()

    return render(request, 'designs/upload_design.html', {'form': form, 'design_images': design_images, 'categories': categories,})  
    
# @login_required
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

# @login_required
def update_profile(request):
    context = {}
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if new_username:
            request.user.username = new_username
            request.user.save()
            context['username_message'] = 'Your username has been updated!'
        else: 
            context['username_error'] = 'Please enter a valid username'

        if new_email:
            request.user.email = new_email
            request.user.save()
            context['email_message'] = 'Your email has been updated!'
        else:
            context['email_error'] = 'Please enter a valid email'

        return render(request, 'user_settings.html', context)

    