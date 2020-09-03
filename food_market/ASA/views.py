from django.shortcuts import render
from django.http import HttpResponse
from product.models import Category, Subcategory



def index(request):

    array = []
    categories = Category.objects.all()
    for category in categories:
        subcategories = Subcategory.objects.filter(category=category)
        cat = [category, [subcategories]]
        array.append(cat)
    context = {'categories': array}
    return render(request, 'ASA/home1.html', context=context)


