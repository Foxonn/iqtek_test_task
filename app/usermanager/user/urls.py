from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from user.views import ListUsersAPIView, UserAPIView

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

app_name = 'user'

urlpatterns = [
    path(
        '',
        cache_page(CACHE_TTL)(ListUsersAPIView.as_view()),
        name='list_users'
    ),
    path(
        '<int:pk>/',
        cache_page(CACHE_TTL)(UserAPIView.as_view()),
        name='user'
    ),
]
