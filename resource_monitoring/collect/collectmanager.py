from .collector import Collector


class CollectManager(object):
    collectors = []

    duration = 2        # seconds

    def _init__(self, data):
        super(CollectManager, self).__init__()
        self.set_config(data)

    def add_collector(self, data):
        data = data or {}
        data['duration'] = self.duration
        clt = Collector(data)
        self.collectors.append(clt)
        clt.start()

    def set_config(self, config):
        if not config:
            return

        if 'duration' in config:
            self.duration = config['duration']


MasterCollector = CollectManager()
