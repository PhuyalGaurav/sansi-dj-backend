from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import models
from .serializers import FollowingSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from urllib.parse import urljoin
import requests
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
import jwt
from jwt.exceptions import ImmatureSignatureError
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserFollowingViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = FollowingSerializer
    queryset = models.UserFollowing.objects.all()

    def get_followers(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id)
        followers = user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)

    def get_following(self, request, user_id=None):
        user = get_object_or_404(User, id=user_id)
        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)


class UserInfoAPIView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ImmatureSignatureError as e:
            return Response({"error": "The token is not yet valid (iat)", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except OAuth2Error as e:
            return Response({"error": "Invalid id_token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")

        if code is None:
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        token_endpoint_url = urljoin("https://oauth2.googleapis.com", "/token")
        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }
        token_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            token_endpoint_url, data=token_data, headers=token_headers)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch token", "details": response.text}, status=response.status_code)

        try:
            token_data = response.json()
        except ValueError as e:
            return Response({"error": "Invalid JSON in token response", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        id_token = token_data.get("id_token")
        if not id_token:
            return Response({"error": "No id_token in response"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the id_token
            decoded_token = jwt.decode(
                id_token, options={"verify_signature": False})
        except ImmatureSignatureError as e:
            return Response({"error": "The token is not yet valid (iat)", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as e:
            return Response({"error": "The token has expired", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError as e:
            return Response({"error": "Invalid id_token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_response = requests.get(
            user_info_url, params={"access_token": token_data.get("access_token")})

        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user info", "details": user_info_response.text}, status=user_info_response.status_code)

        try:
            user_info = user_info_response.json()
        except ValueError as e:
            return Response({"error": "Invalid JSON in user info response", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Process user_info and create or get the user
        email = user_info.get("email")
        if not email:
            return Response({"error": "No email found in user info"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            email=email, defaults={"username": email})

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "message": "Login successful",
            "user_info": user_info,
            "access_token": access_token,
            "refresh_token": refresh_token
        }, status=status.HTTP_200_OK)


class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
