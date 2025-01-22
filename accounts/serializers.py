from rest_framework import serializers
from .models import UserFollowing, Profile, Achievement
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "is_staff",
                  "is_active", "is_superuser", "date_joined"]


class UserFollowingSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    following_user_id = UserSerializer()

    class Meta:
        model = UserFollowing
        fields = ["user_id", "following_user_id", "created"]


class UserProfileSerializer(serializers.ModelSerializer):
    achievements = serializers.StringRelatedField(many=True)
    user = UserSerializer()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["user", "bio", "location", "birth_date", "achievements",
                  "name", "given_name", "family_name", "picture", "followers", "following"]

    def get_followers(self, obj):
        followers = UserFollowing.objects.filter(
            following_user_id=obj.user).values_list('user_id__username', flat=True)
        return list(followers)

    def get_following(self, obj):
        following = UserFollowing.objects.filter(user_id=obj.user).values_list(
            'following_user_id__username', flat=True)
        return list(following)
