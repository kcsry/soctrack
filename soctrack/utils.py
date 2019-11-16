import re
import time

from django.conf import settings
from django.utils.timezone import make_aware, make_naive, utc

re_pattern = re.compile('[^\u0000-\uD7FF\uE000-\uFFFF]+', re.UNICODE)


def sanitize_unicode(u):
    # We may not be able to store all special characters thanks
    # to MySQL's boneheadedness, so accept the minor loss of fidelity
    # in the cached data fields.
    return re_pattern.sub(' ', u)


def could_be_utc(dt):
    if settings.USE_TZ:
        return make_aware(dt, utc)
    else:
        if dt.tzinfo:
            return make_naive(dt, utc)
        else:
            return dt


class RetryError(Exception):
    def __init__(self, fn, tries, exceptions):
        super(RetryError, self).__init__('%s failed after %d tries' % (fn, tries))
        self.exceptions = exceptions


def retry_with_backoff(fn, tries=10, wait=0.5, exception_classes=(Exception,)):
    exceptions = []
    for t in range(tries):
        try:
            return fn()
        except exception_classes as e:
            exceptions.append(e)
            time.sleep(wait * (1.5**t))
    raise RetryError(fn, tries, exceptions)
