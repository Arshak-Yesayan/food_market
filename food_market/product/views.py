from django.shortcuts import render, redirect
from django.http import JsonResponse

from product.models import Product, Category, Subcategory
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

        if category_id.isdigit() and category_id != '':
            where_search.append(f'subcategory_id = {category_id}')

        if price_from != '':
            where_search.append(f'price >= {price_from}')

        if price_to != '':
            where_search.append(f'price <= {price_to}')
        
        if len(where_search) == 0:
            search_form = ''
        else:
            search_form = 'WHERE ' + ' AND '.join(where_search)

        if sort_by == 'name':
            sort_tag = 'title'
            sort_way = 'ASC'
        elif sort_by == 'popular':
            sort_tag = 'likes'
            sort_way = 'DESC'
        elif sort_by == 'price_hl':
            sort_tag = 'price'
            sort_way = 'DESC'
        elif sort_by == 'price_lh':
            sort_tag = 'price'
            sort_way = 'ASC'
        else:
            redirect('all_products')
        
        search_form = f'SELECT * FROM product_product {search_form} ORDER BY {sort_tag} COLLATE NOCASE {sort_way}, title COLLATE NOCASE ASC  LIMIT 10'

        found = Product.objects.raw(search_form)
    except:
        found = Product.objects.raw('SELECT * FROM product_product ORDER BY title COLLATE NOCASE ASC LIMIT 10')
    
    array = []
    categories = Category.objects.all()
    for category in categories:
        subcategories = Subcategory.objects.filter(category=category)
        cat = [category, [subcategories]]
        array.append(cat)

    context = {'products': found, 'categories': array}
    return render(requests, 'product/index.html', context=context)

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

def like(request):
    if request.user.is_authenticated:
        try:
            id = request.GET['id']
            what = request.GET['what']
            product = Product.objects.get(id=id)
            if what == 'like':
                product.likes += 1
            elif what == 'dislike':
                product.dislikes += 1
            product.save()
            return JsonResponse({'result': True})
        except:
            return JsonResponse({'result': False})
    else:
        return JsonResponse({'result': False})