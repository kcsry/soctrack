from django.urls import path
from django.views.decorators.cache import cache_page

from soctrack.views import RecentSocialView

urlpatterns = [
    path('api/social/', cache_page(15)(RecentSocialView.as_view())),
]
