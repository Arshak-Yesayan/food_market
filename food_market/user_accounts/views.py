from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

from user_accounts.models import Verification

import datetime
from random import choice
import string
import emails

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
                            user = User.objects.create_user(username=username, email=email)
                            user.set_password(password1)
                            user.is_active = False
                            date = datetime.datetime.now() + datetime.timedelta(days=1)
                            verify = Verification.objects.create(username=user, date=date)
                            token = get_random_string(16)
                            verify.token = make_password(token)                            

                            sent = False
                            while not sent:
                                message = emails.html(html=f"<h1>If you were logining to our site and your username is {username}, go to this link</h1><a href=\"http://localhost:8000/accounts/verify/?&username={username}&token={token}\">Verify</a>",
                                    subject="Verify your account",
                                    mail_from=('Localhost', 'localhost@localhost.com'))
                                r = message.send(to=f'{email}', smtp={'host': 'aspmx.l.google.com', 'timeout': 5})
                                if r.status_code == 250:
                                    sent= True

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