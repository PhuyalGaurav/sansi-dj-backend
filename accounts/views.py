from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import models
from .serializers import FollowingSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


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
