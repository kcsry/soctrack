# -- encoding: UTF-8 --

from django.conf.urls import url
from django.views.decorators.cache import cache_page

from soctrack.views import RecentSocialView

urlpatterns = [
    url(r'^api/social/$', cache_page(15)(RecentSocialView.as_view())),
]
