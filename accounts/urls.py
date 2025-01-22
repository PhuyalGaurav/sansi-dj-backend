from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ListUsersView, FollowUnfollowView, FollowersView, FollowingView

router = DefaultRouter()
router.register(r'', UserProfileViewSet, basename='profile')
router.register(r'users', ListUsersView, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('follow/<str:username>/',
         FollowUnfollowView.as_view(), name='follow-unfollow'),
    path('followers/<str:username>/', FollowersView.as_view(), name='followers'),
    path('following/<str:username>/', FollowingView.as_view(), name='following'),

]
