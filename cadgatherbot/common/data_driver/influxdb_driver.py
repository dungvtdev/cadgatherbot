import json
import re

import falcon
from eventlet.green import urllib2

import cadgatherbot.config as config
from utils.dbdriver import BaseResourcesDBDriver


def fetch_url(url):
    try:
        return urllib2.urlopen(url).read()
    except (urllib2.URLError, urllib2.HTTPError):
        print("Connection Refuse: URL {0}.".format(url))
    except Exception as e:
        print("UnKnown Error " + e)


class InfluxdbDataDriver(BaseResourcesDBDriver):
    epoch = 's'
    last = '10m'
    mean_duration = '2s'

    _time_filter_string = ""

    def __init__(self, pool, **kwargv):
        super(InfluxdbDataDriver, self).__init__(**kwargv)

        self.pool = pool

    def setting(self, **kwargv):
        super(InfluxdbDataDriver, self).setting(**kwargv)
        if 'epoch' in kwargv:
            self.epoch = kwargv['epoch']
        if 'last' in kwargv:
            self.last = kwargv['last']
            self._time_filter_string = self.get_timefilter_string()
        if 'mean_duration' in kwargv:
            self.mean_duration = kwargv['mean_duration']

    def query(self, endpoint, db_name, metric, **kwarg):
        last = None if 'last' not in kwarg else kwarg['last']
        base = None if 'base' not in kwarg else kwarg['base']

        if last:
            self._time_filter_string = self.get_timefilter_string(base=base, last=last)
            queries = self.get_queries(metric)
        else:
            queries = self.get_queries(metric)

        if not queries:
            return None

        links = map(lambda q: falcon.uri.encode(
            self.get_link(endpoint, db_name, q)), queries)

        # print(links)
        json_list = []
        for body in self.pool.imap(fetch_url, links):
            if body:
                json_list.append(body)

        return self.combine(json_list, metric)

    def combine(self, json_list, metric):
        # create container object
        result = {}

        try:

            for m in metric:
                result[m[0]] = {
                    'container': None if len(m) == 1 else m[1],
                    'data': []
                }

            for json_obj in json_list:
                p_obj = json.loads(json_obj)
                res_list = p_obj['results'][0]['series']
                for res in res_list:
                    lname = res['name']
                    if lname in result:
                        result_item = result[lname]
                        # xet ca truong hop khong co tags cua mot so measurement
                        if 'tags' not in res:
                            can_add = True
                            c_container = None
                        else:
                            c_container = res['tags']['container_name']
                            can_add = not result_item['container'] or result_item[
                                                                          'container'] == c_container

                        if can_add:
                            result_item['data'].append(res)
                            res['container'] = c_container
                            map(res.pop, ['name', 'columns'])
                            if 'tags' in res:
                                res.pop('tags')
        except Exception:
            pass

        return result

    def get_link(self, endpoint, db_name, query):
        param_dict = {
            'epoch': self.epoch,
            'db': db_name,
            'q': query
        }
        link = "{endpoint}/query{params}".format(endpoint=self.protocol_decorate(endpoint),
                                                 params=falcon.to_query_str(param_dict, False, True))
        return link

    def get_queries(self, metric):
        # split cpu measurements
        cpu_measurements = tuple(m for m in metric if 'cpu' in m[0])
        accum_measurements = tuple(
            m for m in metric if m not in cpu_measurements)

        queries = self.get_cpu_queries(
            cpu_measurements) + self.get_accum_queries(accum_measurements)

        return queries

    def get_cpu_queries(self, cpu_metrics):
        if not cpu_metrics:
            return ()

        time_filter = self._time_filter_string
        measurements = ','.join(map(lambda x: x[0], cpu_metrics))

        query = "SELECT derivative(\"value\", 5s)/1000000000 " \
                "FROM {measurements} " \
                "WHERE {timeFilter} " \
                "GROUP BY \"container_name\" fill(null)"

        query = query.format(measurements=measurements, timeFilter=time_filter)

        return (query,)

    def get_accum_queries(self, metrics):
        if not metrics:
            return ()

        time_filter = self._time_filter_string
        measurements = ','.join(map(lambda x: x[0], metrics))
        time_interval = self.mean_duration

        query = "SELECT mean(\"value\") " \
                "FROM {measurements} " \
                "WHERE {timeFilter} " \
                "GROUP BY time({timeInterval}) fill(null)"

        query = query.format(measurements=measurements,
                             timeFilter=time_filter, timeInterval=time_interval)

        return (query,)

    def get_timefilter_string(self, base=None, last=None):
        last = last or self.last
        pattern = r'^(\d+[%s])$' % config.TIME_FILTER_METRIC_ALLOWED

        match = re.match(pattern, last)
        if not match:
            last = self.last

        base = base
        if base:
            pt = r'^\d+[%s]$' % config.TIME_FILTER_METRIC_ALLOWED
            if re.match(pt, base):
                return "time > %s - %s AND time < %s" % (base, last, base)

        return 'time > now() - %s' % last

# class ResourceData(object):
#     measurement = None,
#     container = None,
#     values = []
#     isAll = True

#     def __init__(self, measurement, container='all'):
#         self.measurement = measurement
#         self.container = container
#         self.isAll = self.container == 'all'

#     def add(self, influxdb_dict):
#         c_container = influxdb_dict['tags']['container_name']
#         if self.isAll or self.container == c_container:
#             influxdb_dict['container'] = c_container
#             map(influxdb_dict.pop, ['name', 'tags', 'columns'])
