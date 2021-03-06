from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from user_accounts import views
from .views import profile

urlpatterns = [
    path('register/', views.auth_register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
    path('profile/', profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)