from django.shortcuts import render
from product.models import Product

# Create your views here.
def all_products(requests):
    best = Product.objects.all()[:5]
    context = {'products': best}
    return render(requests, 'product/index.html', context=context)

def spec_product(requests, slug):
    prod = Product.objects.get(slug=slug)
    context = {'product': prod}
    return render(requests, 'product/spec.html', context=context)