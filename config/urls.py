"""
URL configuration for config project.

"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import GoogleLogin, GoogleLoginCallback, LoginPage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('accounts.urls')),
    path('devtest/', include('devtest.urls')),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path(
        "api/v1/auth/google/callback/",
        GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
    path("login/", LoginPage.as_view(), name="login"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('', include('django.contrib.flatpages.urls')),
]
