from django.shortcuts import render
from main.models import Selling_item

# Create your views here.
def items(requests):
    item = Selling_item.objects.all()[1]
    context = {'username': item.username, 'name': item.item_name, 'description': item.item_description, 'image': item.item_image}
    return render(requests, 'main/items.html', context=context)