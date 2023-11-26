from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UploadDesign, ImageUpload


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
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
        fields = ("caption", "image")
    
    # def save(self, commit=True):
    #     design = super(UploadDesignForm, self).save(commit=False)
    #     design.caption = self.cleaned_data["caption"]
    #     design.image = self.cleaned_data["image"]
    #     if commit:
    #         design.save()
    #     return design