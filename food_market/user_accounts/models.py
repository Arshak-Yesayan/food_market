from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Verification(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    date = models.DateField()

    def __str__(self):
        return str(self.username)