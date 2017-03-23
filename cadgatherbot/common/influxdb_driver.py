import re
from cadgatherbot.utils.dbdriver.resources import BaseResourcesDataDriver


class InfluxdbDataDriver(BaseResourcesDataDriver):
    epoch = 's'
    time_filter = '>10m'

    _time_filter_string = ""

    def setting(self, **kwargv):
        super(InfluxdbDataDriver, self).setting(**kwargv)
        if 'epoch' in kwargv:
            self.epoch = kwargv['epoch']
        if 'time_filter' in kwargv:
            self.time_filter = kwargv['time_filter']
            self._time_filter_string = self.get_timefilter_string()

    def query(self, endpoint, metric):
        pass

    def get_cpu_query(self, cpu_metrics):
        time_filter = self._time_filter_string
        measurements = ','.join(map(lambda x: x[0], cpu_metrics))

        query = "SELECT derivative(\"value\", 5s)/1000000000 " \
            "FROM {measurements} " \
            "WHERE {timeFilter} " \
            "GROUP BY \"container_name\" fill(null)"

        query = query.format(measurements=measurements, timeFilter=time_filter)

        return (query,)

    def get_accum_query(self, metrics):
        pass

    def get_timefilter_string(self):
        default = '>10m'
        tf = self.time_filter or default
        pattern = r'(^[><]*[=]*)\s*(\d*[smhd])$'

        match = re.match(pattern, tf)
        if not match:
            match = re.match(pattern, default)

        return 'now() ' + match.groups()[0] + " " + match.groups()[1]
