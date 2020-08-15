from django.shortcuts import render

# Create your views here.
def main(requests):
    return render(requests, 'index.html')