from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Verification(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    date = models.DateField()

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=150)
    photo = models.ImageField(default="profile_pics/default.jpg", upload_to="profile_pics", blank=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
