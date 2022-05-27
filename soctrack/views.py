import datetime

from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic import View

from soctrack.models import Post


class RecentSocialView(View):
    def get(self, request, *args, **kwargs):
        cutoff = now() - datetime.timedelta(hours=int(request.GET.get('hours', 7)))
        posts = (
            Post.objects.filter(posted_on__gte=cutoff, hidden=False)
            .order_by('-posted_on')
            .defer('blob')[:100]
        )
        return JsonResponse([p.to_json() for p in posts], safe=False)
