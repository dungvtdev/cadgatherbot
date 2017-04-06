from .collector import Collector
import time


class CollectManager(object):
    collectors = []

    query_pattern = ""
    collected_metrics = []

    duration = 2        # seconds
    backward_time = 0    # seconds, current = time.time() - backward_time

    def _init__(self, data):
        super(CollectManager, self).__init__()
        self.set_config(data)

    def add_collector(self, data):
        data = data or {}
        self.setup_collector_data(data)

        clt = Collector(data)
        self.collectors.append(clt)
        clt.start()

    def setup_collector_data(self, data):
        data['duration'] = self.duration
        data['current_time'] = time.time() - self.backward_time
        data['endpoint'] = 'http://localhost:8090'
        data['user_id'] = '1'
        data['machine_id'] = '1'
        data['query_pattern'] = self.query_pattern
        data['collected_metrics'] = self.collected_metrics

    def set_config(self, config):
        if not config:
            return

        self.duration = config.get('duration', self.duration)
        self.query_pattern = config.get('query_pattern', self.query_pattern)
        self.collected_metrics = config.get('collected_metrics', self.collected_metrics)
        self.backward_time = config.get('backward_time', self.backward_time)

MasterCollector = CollectManager()
