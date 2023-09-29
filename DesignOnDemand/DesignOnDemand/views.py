from django.shortcuts import render
from .models import DesignProduct

def main_page(request):
    return render(request, 'designondemand/main_page.html')

# Path: DesignOnDemand/DesignOnDemand/views.py
def main_page(request):
    featured_products = DesignProduct.objects.all()[:4]  # Displaying 4 featured products
    return render(request, 'appname/main_page.html', {'featured_products': featured_products})