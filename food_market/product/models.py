from django.db import models
from django.contrib.auth.models import User

import os
from uuid import uuid4

# Create your models here.
def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'product/{}.{}'.format(instance.title, extension)

class Category(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=64, null=False, unique=True)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to=upload_location, max_length=255, null=True, blank=True, default='product/default.png')
    likes = models.IntegerField(default=0, null=False)
    dislikes = models.IntegerField(default=0, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.title

class Like(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    like_dislike = models.BooleanField()

    def __str__(self):
        return str(self.username) + ' - ' + str(self.product)