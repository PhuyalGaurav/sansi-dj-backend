"""
URL configuration for config project.

"""
from django.contrib import admin
from django.urls import path, include
from socialauth.google import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('profile/', include('accounts.urls')),
    path('devtest/', include('devtest.urls')),
]
