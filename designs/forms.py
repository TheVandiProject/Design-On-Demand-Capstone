from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# from .models import UploadDesign, UploadDesignerDesign
# from django.db import models
from .models import *
from all_data import models as all_data_models


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = all_data_models.Users
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class UploadDesignForm(forms.Form):
    class Meta:
        model = UploadDesign
        fields = '__all__'

        
#UserUpdateForm to update a username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = all_data_models.Users
        fields = ['username', 'email']

#ProfileUpdateForm to update image.
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = all_data_models.Designer
        fields = ['username', 'email']
        
class UploadDesignerDesignForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
    queryset=all_data_models.Category.objects.all(),
    widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = all_data_models.UploadDesignerDesign
        fields = ['image', 'categories']