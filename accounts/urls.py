from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserFollowingViewSet, UserInfoAPIView

router = DefaultRouter()
router.register(r'follow', UserFollowingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('info/<int:user_id>', UserInfoAPIView.as_view(), name='user-info'),
    path('followers/<int:user_id>',
         UserFollowingViewSet.as_view({'get': 'get_followers'}), name='user-followers'),
    path('following/<int:user_id>',
         UserFollowingViewSet.as_view({'get': 'get_following'}), name='user-following'),
]
