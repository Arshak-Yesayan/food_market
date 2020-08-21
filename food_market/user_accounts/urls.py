from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('register/', views.auth_register, name='register'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)