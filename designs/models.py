from django.db import models
from PIL import Image # Pillow library for image resizing


class UploadDesign(models.Model):
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='media/uploaded')  # Store design images

    def __str__(self):
        return self.caption

class DesignProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')  # Store product images in the 'products' directory
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the uploaded image with Pillow
        img = Image.open(self.image.path)

        # Resize the image if needed
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploaded/')