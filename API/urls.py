from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import UserViewSet, AdminViewSet, PostViewSet

router = DefaultRouter()
router.register('users',UserViewSet,basename='users')
router.register('admins',AdminViewSet,basename='admins')
router.register('posts',PostViewSet,basename='posts')

urlpatterns = [
    path('',include(router.urls))
]
