from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(requests):
#     if requests.user.is_authenticated:
#         print(requests.user.username, requests.user.password)
    return render(requests, 'main/index.html')

def auth_register(requests):
    if requests.method == 'POST':
        form = UserCreationForm(requests.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(requests, user)
            return redirect('main')

    return render(requests, 'registration/register.html')

def auth_login(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(requests, user)
            return redirect('main')

    return render(requests, 'registration/login.html')

def auth_logout(requests):
    if requests.user.is_authenticated:
        logout(requests)
        return redirect('main')
    return render(requests, 'registration/logout.html')
