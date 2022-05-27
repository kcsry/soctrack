from django.db import models
from django.utils.timezone import make_aware, utc
from jsonfield.fields import JSONField

MEDIUM_CHOICES = [
    ('ig', 'Instagram'),
    ('tw', 'Twitter'),
]


class Tag(models.Model):
    tag = models.CharField(max_length=64, db_index=True)


class Post(models.Model):
    medium = models.CharField(max_length=4, choices=MEDIUM_CHOICES)
    identifier = models.CharField(max_length=64)
    downloaded_on = models.DateTimeField(auto_now_add=True)
    posted_on = models.DateTimeField(blank=True, null=True, db_index=True)
    hidden = models.BooleanField(db_index=True, default=False)
    post_url = models.URLField(max_length=128, blank=True)
    avatar_url = models.URLField(max_length=128, blank=True)
    primary_image_url = models.URLField(max_length=128, blank=True)
    tags = models.ManyToManyField(Tag)

    author_name = models.CharField(max_length=64, blank=True)
    message = models.CharField(max_length=140, blank=True)
    blob = JSONField()

    class Meta:
        unique_together = (
            (
                'medium',
                'identifier',
            ),
        )

    def add_text_tags(self, tags):
        for tag in set(tags):
            try:
                self.tags.add(Tag.objects.get_or_create(tag=tag)[0])
            except:
                pass

    def to_json(self):
        time = make_aware(self.posted_on, utc)
        return {
            'medium': self.medium,
            'id': self.identifier,
            'posted_on': time.isoformat(),
            'post_url': self.post_url,
            'avatar_url': self.avatar_url,
            'primary_image_url': self.primary_image_url,
            'author_name': self.author_name,
            'message': self.message,
        }
