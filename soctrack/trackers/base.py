class BaseTracker:
    def track_search(self, search):
        raise NotImplementedError('Ni!')

    def ingest(self, datum):
        raise NotImplementedError('Ni!')
