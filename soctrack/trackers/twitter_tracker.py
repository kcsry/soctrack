import datetime
from email.utils import parsedate_tz

import twitter
from django.conf import settings

from soctrack.models import Post
from soctrack.trackers.base import BaseTracker
from soctrack.utils import could_be_utc, retry_with_backoff, sanitize_unicode


def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime.datetime(*time_tuple[:6])
    return could_be_utc(dt - datetime.timedelta(seconds=time_tuple[-1]))


class TwitterTracker(BaseTracker):
    medium = 'tw'

    def __init__(self):
        self.client = twitter.Twitter(
            auth=twitter.OAuth(
                token=settings.SOCTRACK_TWITTER_TOKEN,
                token_secret=settings.SOCTRACK_TWITTER_TOKEN_SECRET,
                consumer_key=settings.SOCTRACK_TWITTER_CONSUMER_KEY,
                consumer_secret=settings.SOCTRACK_TWITTER_CONSUMER_SECRET,
            )
        )

    def track_search(self, search):
        def get_result():
            return self.client.search.tweets(q=search, count=100, include_entities=True, result_type='recent')

        result = retry_with_backoff(get_result)
        for post in result.get('statuses', []):
            self._process_post(post)

    def ingest(self, datum):
        return self._process_post(datum)

    def _process_post(self, status):
        """
        :type status: dict
        """
        post_id = status['id_str']
        if Post.objects.filter(medium=self.medium, identifier=post_id).exists():
            return False

        try:
            user_name = status['user']['screen_name']
        except KeyError:
            user_name = status['from_user']  # Old-school format

        url = f'https://twitter.com/{user_name}/status/{post_id}'
        entities = status.get('entities', {})

        primary_image_url = ''
        for media in entities.get('media', ()):
            if media.get('type') == 'photo':
                primary_image_url = media['media_url_https']
                break

        try:
            avatar_url = status['user']['profile_image_url']
        except KeyError:
            avatar_url = status['profile_image_url']  # Old-school format

        # Add it!

        post = Post(
            medium=self.medium,
            identifier=post_id,
            post_url=url,
            posted_on=to_datetime(status['created_at']),
            primary_image_url=primary_image_url,
            author_name=f'@{user_name}',
            avatar_url=avatar_url,
            message=sanitize_unicode(status['text'][:140]),
            blob=status,
        )
        post.save()
        hashtags = entities.get('hashtags', ())
        if hashtags:
            post.add_text_tags([t['text'] for t in hashtags])
        return post
