import time
import threading


class Collector(threading.Thread):
    data = None,
    running = False,
    default_duration = 20       # seconds

    def __init__(self, data):
        threading.Thread.__init__(self)

        self.setting(data)

    def setting(self, data):
        self.data = data

    def run(self):
        query = self.get_query()
        duration = self.data.get('duration', self.default_duration) if self.data else self.default_duration
        self.running = True

        while True:
            if not self.running:
                break

            old_t = time.time()

            data = self.get_data(query)
            str_data = self.parse_data_as_influx(data)
            self.write_data(str_data)

            t = duration - (time.time() - old_t)
            t = t if t > 0 else 0

            time.sleep(t)

    def get_data(self, query):
        print('get data')

    def write_data(self, data):
        print('write data')

    def parse_data_as_influx(self, data):
        print('parse data')

    def get_query(self):
        pass
