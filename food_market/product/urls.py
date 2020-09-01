from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from product import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('get_json', views.get_json, name='json'),
    path('<str:title>/', views.spec_product, name='spec_product'),
    path('categories/<str:categories>/', views.category, name='category'),
    path('subcategories/<str:subcategories>/', views.subcategory, name='subcategory'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)