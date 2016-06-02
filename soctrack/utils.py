# -- encoding: UTF-8 --

import re

from django.conf import settings
from django.utils.timezone import make_aware, make_naive, utc

re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]+', re.UNICODE)


def sanitize_unicode(u):
    # We may not be able to store all special characters thanks
    # to MySQL's boneheadedness, so accept the minor loss of fidelity
    # in the cached data fields.
    return re_pattern.sub(u' ', u)


def could_be_utc(dt):
    if settings.USE_TZ:
        return make_aware(dt, utc)
    else:
        if dt.tzinfo:
            return make_naive(dt, utc)
        else:
            return dt
