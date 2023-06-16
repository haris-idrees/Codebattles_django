from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import UserViewSet, AdminViewSet, PostViewSet,ProblemViewSet

router = DefaultRouter()
router.register('users',UserViewSet,basename='users')
router.register('admins',AdminViewSet,basename='admins')
router.register('posts',PostViewSet,basename='posts')
router.register('problems',ProblemViewSet,basename='problems')

urlpatterns = [
    path('',include(router.urls))
]
