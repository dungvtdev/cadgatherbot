import time
import threading
import requests
import json


def mean_value(values):
    return sum(map(lambda x: x[1], values)) * 1.0 / len(values)


class Collector(threading.Thread):
    data = None,
    running = False,
    default_duration = 20  # seconds

    duration = 0,
    endpoint = ""
    user_id = ""
    machine_id = ""
    metrics = []

    current_time = 0

    def __init__(self, data):
        threading.Thread.__init__(self)

        self.setting(data)

    def setting(self, data):
        self.data = data
        self.duration = self.data.get('duration', self.default_duration) if self.data else self.default_duration
        self.endpoint = self.data["endpoint"]
        self.user_id = self.data["user_id"]
        self.machine_id = self.data["machine_id"]
        self.current_time = self.data.get('current_time', time.time())
        self.metrics = self.data['collected_metrics']

    def run(self):
        self.running = True
        query = self.get_base_query()

        while True:
            if not self.running:
                break
            old_t = time.time()

            data = self.get_data(query)
            print(data)

            if data:
                str_data = self.parse_data_as_influx(data)
                self.write_data(str_data)

            t = self.duration - (time.time() - old_t)
            t = t if t > 0 else 0

            time.sleep(t)
            self.current_time += self.duration

    def get_data(self, query):
        payload = {
            'last': '%ds' % self.duration,
            'base': '%ds' % self.current_time,
            'metric': self.metrics
        }
        try:
            r = requests.get(query, params=payload)
            print(r.url)
            return r.content
        except requests.exceptions.RequestException as e:
            print(e.message)
            return None

    def write_data(self, data):
        print(data)

    def parse_data_as_influx(self, data):
        print('parse data')

        d = []

        pydata = json.loads(data)
        cur_time = (self.current_time - self.duration/2)
        for k, mdata in pydata['data'].items():
            if mdata['data']:
                v = mean_value(mdata['data'][0]['values'])
                s = "%s value=%s %s" %(k, v, cur_time)
                d.append(s)

        payload = "\n".join(d)
        return payload

    def get_base_query(self):
        query = self.data['query_pattern']
        query = query.format(endpoint=self.endpoint,
                             user_id=self.user_id,
                             machine_id=self.machine_id)
        return query
