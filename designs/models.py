from django.db import models
from PIL import Image # Pillow library for image resizing
from django.contrib.auth.models import User


class UploadDesign(models.Model):
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='uploaded')  # Store design images

    def __str__(self):
        return self.caption

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='media/uploaded')

class Designer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='user-icon-default-96.png', upload_to='profile_pics')

    def __str__(self):
        return self.user.username #show how we want it to be displayed
    
     # Override the save method of the model
    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image
            
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class UploadDesignerDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='designer-uploads/')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.user.username} - {self.image}'
