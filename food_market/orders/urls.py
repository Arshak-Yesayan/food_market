from . import views
from django.urls import path, include


urlpatterns = [
    path('basket_adding/', views.basket_adding, name='basket_adding'),

]