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
        if datetime.datetime(user_verification.date.year, user_verification.date.month, user_verification.date.day) < new_date:
            user_account = User.objects.get(username=user_verification.username)
            user_account.delete()

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

# Create your views here.

def auth_register(request):
    context = {'message': None}
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        token = get_random_string(16)
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        result = try_register(username, password1, password2, email, token, date)
        if result[0]:
            send_mail('Verify to ASA',
            f'Go to this link to verify {settings.DOMAIN_NAME}/accounts/verify/?username={username}&token={token}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False)

            result[1].save()
            result[2].save()
            return redirect('login')
        else:
            context['message'] = result[1]
    return render(request, 'accounts/register.html', context=context)


def verify(request):
    context = {'verified': False}

    update_verification()

    try:
        username = request.GET['username']
        token = request.GET['token']
        user = User.objects.get(username=username)
        verify = Verification.objects.get(username=user)
        if check_password(token, verify.token):
            verify.delete()
            user.is_active = True
            user.save()
            context['verified'] = True
    except:
        pass
    return render(request, 'accounts/verify.html', context=context)


def auth_login(request):
    context = {'message': None}
    if request.method == 'POST':
        if request.POST['username'] == '' or request.POST['password'] == '':
            context['message'] = 'Write something to the fields.'
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                context['message'] = 'Wrong username or password.'

    return render(request, 'accounts/login.html', context=context)


def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
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