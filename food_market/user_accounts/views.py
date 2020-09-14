from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings

from user_accounts.models import Verification
from django.contrib.auth.decorators import login_required
import datetime
from random import choice
import string
from user_accounts.forms import ProfileForm, UserUpdateForm



def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(choice(letters) for i in range(length))


def update_verification():
    users_verifications = Verification.objects.all()
    new_date = datetime.datetime.utcnow()
    for user_verification in users_verifications:
        if datetime.datetime(user_verification.date.year, user_verification.date.month,
                             user_verification.date.day) < new_date:
            user_account = User.objects.get(username=user_verification.username)
            user_account.delete()


# Create your views here.

def auth_register(requests):
    context = {'message': None}
    if requests.method == 'POST':
        username = requests.POST['username']
        password1 = requests.POST['password1']
        password2 = requests.POST['password2']
        email = requests.POST['email']
        if not (username == '' or password1 == '' or password2 == '' or email == ''):
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if password1 == password2:
                        if len(password1) >= 8:
                            user = User(username=username, email=email)
                            user.set_password(password1)
                            user.is_active = False
                            date = datetime.datetime.now() + datetime.timedelta(days=1)
                            verify = Verification(username=user, date=date)
                            token = get_random_string(16)
                            verify.token = make_password(token)

                            send_mail('Verify to ASA',
                            f'Go to this link to verify {settings.DOMAIN_NAME}/accounts/verify/?username={username}&token={token}',
                            settings.EMAIL_HOST_USER,
                            [email],
                            fail_silently=False)

                            user.save()
                            verify.save()
                            return redirect('login')
                        else:
                            context['message'] = 'Passwords length is to less.'
                    else:
                        context['message'] = 'Passwords must be same.'
                else:
                    context['message'] = 'Email already exists.'
            else:
                context['message'] = 'Username already exists.'
        else:
            context['message'] = 'Write something to the fields.'
    return render(requests, 'accounts/register.html', context=context)


def verify(requests):
    context = {'verified': False}

    update_verification()

    try:
        username = requests.GET['username']
        token = requests.GET['token']
        user = User.objects.get(username=username)
        verify = Verification.objects.get(username=user)
        if check_password(token, verify.token):
            verify.delete()
            user.is_active = True
            user.save()
            context['verified'] = True
    except:
        pass
    return render(requests, 'accounts/verify.html', context=context)


def auth_login(requests):
    context = {'message': None}
    if requests.method == 'POST':
        if requests.POST['username'] == '' or requests.POST['password'] == '':
            context['message'] = 'Write something to the fields.'
        else:
            username = requests.POST['username']
            password = requests.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(requests, user)
                return redirect('index')
            else:
                context['message'] = 'Wrong username or password.'

    return render(requests, 'accounts/login.html', context=context)


def auth_logout(requests):
    if requests.user.is_authenticated:
        logout(requests)
    return redirect('index')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST,
                             request.FILES,
                             instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm()

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'accounts/profile.html', context)
