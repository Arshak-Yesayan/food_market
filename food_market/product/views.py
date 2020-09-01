from django.shortcuts import render, redirect
from product.models import Product, Category, Subcategory
from django.http import JsonResponse
from random import randint

# Create your views here.
def all_products(requests):
    try:
        name = requests.GET['name']
        category_id = requests.GET['category']
        price_from = requests.GET['from']
        price_to = requests.GET['to']
        sort_by = requests.GET['sort']
        where_search = []

        if name != '':
            where_search.append(f"title LIKE '%{name}%'")

        if category_id.isdigit():
            where_search.append(f'subcategory_id = {category_id}')

        if price_from != '':
            where_search.append(f'price >= {price_from}')

        if price_to != '':
            where_search.append(f'price <= {price_to}')
        
        if len(where_search) == 0:
            search_form = ''
        else:
            search_form = 'WHERE ' + ' AND '.join(where_search)

        if sort_by[-1] == '+':
            sort_way = 'ASC'
        elif sort_by[-1] == '-':
            sort_way = 'DESC'
        else:
            redirect('all_products')
        
        if sort_by[:-1] in ['title', 'likes', 'price']:
            sort_tag = sort_by[:-1]
        else:
            redirect('all_products')
        
        search_form = f'SELECT * FROM product_product {search_form} ORDER BY {sort_tag} {sort_way} LIMIT 10'

        found = Product.objects.raw(search_form)
    except:
        found = Product.objects.raw('SELECT * FROM product_product ORDER BY title ASC LIMIT 10')
    subcategories = Subcategory.objects.all()
    context = {'products': found, 'subcategories': subcategories}
    return render(requests, 'product/index.html', context=context)

def get_json(requests):
    try:
        number = int(requests.GET['number'])
    except:
        number = 500000
    return JsonResponse({'number': str(randint(number - 10000, number + 10000))})

def spec_product(requests, title):
    try:
        prod = Product.objects.get(title=title)
    except:
        return redirect('all_products')
    category = Subcategory.objects.get(name=prod.subcategory).category
    context = {'product': prod, 'category': category}
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
        products = Product.objects.filter(subcategory=subcat)
    except:
        return redirect('all_products')
    context = {'subcategory': subcat, 'other_cats': other_cats, 'products': products}
    return render(requests, 'product/subcategory.html', context=context)