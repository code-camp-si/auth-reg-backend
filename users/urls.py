from django.urls import path, include
from .views import register_user, login_user, user_profile
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('profile/', user_profile),
]