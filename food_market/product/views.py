from django.shortcuts import render, redirect
from product.models import Product, Category, Subcategory

# Create your views here.
def all_products(requests):
    best = Product.objects.all()[:5]
    context = {'products': best}
    return render(requests, 'product/index.html', context=context)

def spec_product(requests, title):
    try:
        prod = Product.objects.get(title=title)
    except:
        return redirect('all_products')
    context = {'product': prod}
    return render(requests, 'product/spec.html', context=context)

def category(requests, categories):
    try:
        cat = Category.objects.get(name=categories)
        other_cats = Category.objects.all()
        subcats = Subcategory.objects.filter(category=cat)
    except:
        return redirect('all_products')
    context = {'category': cat, 'other_cats': other_cats, 'sub_cats': subcats}
    return render(requests, 'product/category.html', context=context)

def subcategory(requests, subcategories):
    try:
        subcat = Subcategory.objects.get(name=subcategories)
        other_cats = Subcategory.objects.filter(category=subcat.category)
    except:
        return redirect('all_products')
    context = {'subcategory': subcat, 'other_cats': other_cats}
    return render(requests, 'product/subcategory.html', context=context)