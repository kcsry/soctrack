from django.core.management.base import BaseCommand

from soctrack.trackers import tracker_classes


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('searches', nargs='+')

    def handle(self, searches, **options):
        searches = sorted(searches)
        tracker_objects = [klass() for klass in tracker_classes]
        for search in searches:
            for tracker in tracker_objects:
                tracker.track_search(search)
