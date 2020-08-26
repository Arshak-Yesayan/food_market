from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Selling_item(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=64)
    item_description = models.TextField()
    item_image = models.ImageField(upload_to="selling_items", default="selling_items/default.jpg")

    def __str__(self):
        return f'{self.username} - {self.item_name}'