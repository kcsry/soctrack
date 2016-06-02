# -- encoding: UTF-8 --

from __future__ import print_function

import json
from collections import Counter

from django.core.management.base import BaseCommand

from soctrack.trackers import tracker_classes


class Command(BaseCommand):
    def handle(self, medium, filename, **options):
        tracker = None
        for klass in tracker_classes:
            if klass.medium == medium:
                tracker = klass()

        if not tracker:
            print("Could not find tracker for medium %r." % medium)
            return

        with open(filename, "rb") as in_f:
            data = json.load(in_f)

        results = Counter()

        for datum in data:
            results[bool(tracker.ingest(datum))] += 1

        print("Results:", results)
