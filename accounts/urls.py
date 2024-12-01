from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserFollowingViewSet, ListUsersView

router = DefaultRouter()
router.register(r'', UserProfileViewSet, basename='profile')
router.register(r'follow', UserFollowingViewSet, basename='follow')
router.register(r'users', ListUsersView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('unfollow/',
         UserFollowingViewSet.as_view({'delete': 'destroy'}), name='unfollow'),
]
