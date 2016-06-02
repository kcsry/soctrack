# -- encoding: UTF-8 --
class BaseTracker(object):
    def track_search(self, search):
        raise NotImplementedError("Ni!")

    def ingest(self, datum):
        raise NotImplementedError("Ni!")
