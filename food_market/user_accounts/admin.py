from django.contrib import admin
from user_accounts.models import Verification
from .models import Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Verification)