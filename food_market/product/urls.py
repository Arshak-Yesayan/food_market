from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from product import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('<str:title>/', views.spec_product, name='spec_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)