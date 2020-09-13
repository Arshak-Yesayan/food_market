from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User

from product.models import Product, Category, Subcategory, Like
from random import randint

# Create your views here.
def all_products(request):
    try:
        name = request.GET['name']
        category_id = request.GET['category']
        price_from = request.GET['from']
        price_to = request.GET['to']
        sort_by = request.GET['sort']
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

        sort_dict = {'name': ['title', 'ASC'], 'popular': ['likes', 'DESC'], 'price_hl': ['price', 'DESC'], 'price_lh': ['price', 'ASC']}

        if sort_by in sort_dict.keys():
            sort_tag = sort_dict[sort_by][0]
            sort_way = sort_dict[sort_by][1]
        else:
            redirect('all_products')

        found = Product.objects.raw(f'SELECT * FROM product_product {search_form} ORDER BY {sort_tag} COLLATE NOCASE {sort_way}, title COLLATE NOCASE ASC  LIMIT 10')
        product_array = []
        try:
            user = User.objects.get(username=request.user.username)
            for prod in found:
                try:
                    like_row = Like.objects.get(username=user, product=prod)
                    liked = like_row.like
                    disliked = like_row.dislike
                except:
                    liked = False
                    disliked = False
                product_array.append( [prod, liked, disliked] )
        except:
            for prod in found:
                product_array.append( [prod, False, False] )
    except:
        found = Product.objects.raw('SELECT * FROM product_product ORDER BY title COLLATE NOCASE ASC LIMIT 10')
        product_array = []
        try:
            user = User.objects.get(username=request.user.username)
            for prod in found:
                try:
                    like_row = Like.objects.get(username=user, product=prod)
                    liked = like_row.like
                    disliked = like_row.dislike
                except:
                    liked = False
                    disliked = False
                product_array.append( [prod, liked, disliked] )
        except:
            for prod in found:
                product_array.append( [prod, False, False] )
    
    array = []
    categories = Category.objects.all()
    for category in categories:
        subcategories = Subcategory.objects.filter(category=category)
        cat = [category, [subcategories]]
        array.append(cat)

    context = {'products': product_array, 'categories': array}
    return render(request, 'product/products.html', context=context)

def spec_product(request, title):
    try:
        prod = Product.objects.get(title=title)
        try:
            user = User.objects.get(username=request.user.username)
            like_row = Like.objects.get(username=user, product=prod)
            liked = like_row.like
            disliked = like_row.dislike
        except:
            liked = False
            disliked = False
    except:
        return redirect('all_products')
    category = Subcategory.objects.get(name=prod.subcategory).category
    context = {'product': prod, 'category': category, 'liked': liked, 'disliked': disliked}
    return render(request, 'product/product.html', context=context)

def category(request, categories):
    try:
        cat = Category.objects.get(name=categories)
        other_cats = Category.objects.all()
        subcats = Subcategory.objects.filter(category=cat)
    except:
        return redirect('all_products')
    context = {'category': cat, 'other_cats': other_cats, 'sub_cats': subcats}
    return render(request, 'product/category.html', context=context)

def subcategory(request, subcategories):
    try:
        subcat = Subcategory.objects.get(name=subcategories)
        other_cats = Subcategory.objects.filter(category=subcat.category)
        products = Product.objects.filter(subcategory=subcat)
    except:
        return redirect('all_products')
    context = {'subcategory': subcat, 'other_cats': other_cats, 'products': products}
    return render(request, 'product/subcategory.html', context=context)

def like(request):
    if request.user.is_authenticated:
        try:
            id = request.GET['id']
            what = request.GET['what']
            user = User.objects.get(username=request.user.username)
            products = Product.objects.filter(id=id)
            if products.exists():
                product = products[0]
                likes = Like.objects.filter(username=user, product=product)
                if likes.exists():
                    like_row = likes[0]
                    if what == 'like':
                        if like_row.like == True:
                            like_row.like = False
                            product.likes -= 1
                            done = 'd_l'
                        elif like_row.dislike == True:
                            like_row.like = True
                            like_row.dislike = False
                            product.likes += 1
                            product.dislikes -= 1
                            done = 'd_to_l'
                        else:
                            like_row.like = True
                            product.likes += 1
                            done = 'l'
                    elif what == 'dislike':
                        if like_row.dislike == True:
                            like_row.dislike = False
                            product.dislikes -= 1
                            done = 'd_d'
                        elif like_row.like == True:
                            like_row.dislike = True
                            like_row.like = False
                            product.dislikes += 1
                            product.likes -= 1
                            done = 'l_to_d'
                        else:
                            like_row.dislike = True
                            product.dislikes += 1
                            done = 'd'
                else:
                    if what == 'like':
                        product.likes += 1
                        like_row = Like(username=user, product=product, like=True)
                        done = 'l'
                    elif what == 'dislike':
                        product.dislikes += 1
                        like_row = Like(username=user, product=product, dislike=True)
                        done = 'd'
                like_row.save()
                product.save()
            else:
                return JsonResponse({'result': False})
            return JsonResponse({'result': True, 'done': done})
        except:
            return JsonResponse({'result': False})
    else:
        return JsonResponse({'result': False})

def add_cart(request):
    try:
        id = request.GET['id']
        count = request.GET['count']
        print(id, count)
        return JsonResponse({'result': True})
    except:
        return JsonResponse({'result': False})