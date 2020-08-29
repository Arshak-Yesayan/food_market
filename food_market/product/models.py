from django.db import models
# from django.template.defaultfilters import slugify

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
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0, null=False)
    # slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    # def delete(self,*args,**kwargs):
    #     if os.path.isfile(self.image.path):
    #         os.remove(self.image.path)

    #     super(Product, self).delete(*args,**kwargs)