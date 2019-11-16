import datetime

import requests
from django.conf import settings

from soctrack.models import Post
from soctrack.trackers.base import BaseTracker
from soctrack.utils import could_be_utc, sanitize_unicode


class InstagramTracker(BaseTracker):
    medium = 'ig'

    def track_search(self, search):
        url = 'https://api.instagram.com/v1/tags/%s/media/recent' % search.strip('#')
        resp = requests.get(
            url,
            params={
                'client_id': getattr(settings, 'SOCTRACK_INSTAGRAM_CLIENT_ID', ''),
                'access_token': getattr(settings, 'SOCTRACK_INSTAGRAM_ACCESS_TOKEN', ''),
                'count': 100,
            }
        )
        resp.raise_for_status()
        data = resp.json()
        for post in data['data']:
            self._process_post(post)

    def ingest(self, datum):
        return self._process_post(datum)

    def _process_post(self, post_data):
        post_id = post_data['id']
        if Post.objects.filter(medium=self.medium, identifier=post_id).exists():
            return False
        if post_data.get('caption'):
            caption_text = post_data['caption']['text'][:140]
        else:
            caption_text = ""
        posted_on = could_be_utc(datetime.datetime.utcfromtimestamp(int(post_data['created_time'])))
        post = Post(
            medium=self.medium,
            identifier=post_id,
            post_url=post_data['link'],
            posted_on=posted_on,
            primary_image_url=post_data['images']['standard_resolution']['url'],
            avatar_url=post_data['user']['profile_picture'],
            author_name=sanitize_unicode(post_data['user']['username']),
            message=sanitize_unicode(caption_text),
            blob=post_data
        )
        post.save()
        post.add_text_tags(post_data['tags'])
        return post
