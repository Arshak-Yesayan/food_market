from django.contrib.auth.models import User
from rango import forms
from datetime import datetime
from user_accounts.models import Profile


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


YEARS = [x for x in range(1940, datetime.now().year + 1)]


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'email', 'photo']
