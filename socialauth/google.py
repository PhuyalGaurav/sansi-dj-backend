from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings

GOOGLE_SECRETS = getattr(settings, 'GOOGLE_SECRETS', None)

# if you want to use Authorization Code Grant, use this


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_SECRETS['redirect_url']
    client_class = OAuth2Client
