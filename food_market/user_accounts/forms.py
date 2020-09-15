from django.contrib.auth.models import User
from datetime import datetime
from user_accounts.models import Profile
from django import forms
from django.contrib.auth.hashers import make_password

from user_accounts.models import Verification

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


YEARS = [x for x in range(1940, datetime.now().year + 1)]


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']

def try_register(username, password1, password2, email, token, date):
    if not (username == '' or password1 == '' or password2 == '' or email == ''):
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if password1 == password2:
                    if len(password1) >= 8:
                        user = User(username=username, email=email)
                        user.set_password(password1)
                        user.is_active = False
                        verify = Verification(username=user, date=date)
                        verify.token = make_password(token)

                        return True, user, verify
                    else:
                        message = 'Passwords length is to less.'
                else:
                    message = 'Passwords must be same.'
            else:
                message = 'Email already exists.'
        else:
            message = 'Username already exists.'
    else:
        message = 'Write something to the fields.'
    return False, message