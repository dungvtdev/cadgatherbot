import json
import re

import falcon

import cadgatherbot.config as config
from cadgatherbot.common.data_driver import InfluxdbDataDriver
from cadgatherbot.services import InjectionManager as injector
from utils.dbdriver.simple_relationdb import SimpleDictDBDriver

(coreThreadPool,) = injector.inject('CORE_THREAD_POOL')


class MonitoringController(object):
    def __init__(self, user_db, resource_db):
        self.user_db = user_db
        self.resource_db = resource_db

    def get(self, req, resp, user_id, machine_id, metric, **kwarg):
        # last = None if 'last' not in kwarg else kwarg['last']
        # base = None if 'base' not in kwarg else kwarg['base']

        metric = self.parse_metric(metric)
        info = self.user_db.query('endpoint', 'db').key(
            'users', user_id).key('machines', machine_id).run()
        if not info:
            raise falcon.HTTPBadRequest(
                'Database not found user_id {0} and machine_id {1}'.format(user_id, machine_id))

        endpoint = info['endpoint']
        db = info['db']

        result = self.resource_db.query(endpoint,
                                        db,
                                        metric,
                                        **kwarg)

        data = self.post_process_resources_data(metric, result)

        resp.body = data

        return data

    def parse_metric(self, metric):
        # hien tai chi ho tro 1 sub partial, ex "cpu_usage_total./docker"
        if not metric:
            return []

        if not isinstance(metric, list):
            metric = [metric, ]

        return map(lambda x: tuple(x.strip().split('.')), metric)

    def post_process_resources_data(self, metric, data):
        result = {
            'data': data
        }
        return json.dumps(result)


class MonitoringGather(object):
    def __init__(self, user_db, resource_db):
        self.controller = MonitoringController(user_db, resource_db)

    def on_get(self, req, resp, user_id):
        if "machine" not in req.params:
            raise falcon.HTTPBadRequest(
                "Get resources monitoring need machine_id")

        machine_id = req.params['machine']

        if 'base' in req.params:
            base = req.params['base']
            if not match_time_filter_metric(base):
                raise falcon.HTTPBadRequest(
                    'The "base" params must match {number}[%s]' % config.TIME_FILTER_METRIC_ALLOWED)
        else:
            base = None

        if 'last' in req.params:
            last = req.params['last']
            if not match_time_filter_metric(last):
                raise falcon.HTTPBadRequest(
                    'The "last" params must match {number}[%s]' % config.TIME_FILTER_METRIC_ALLOWED)
        else:
            last = None

        metric = None if 'metric' not in req.params else req.params['metric']

        self.controller.get(req, resp, user_id, machine_id, metric, last=last, base=base)


def match_time_filter_metric(time_val):
    return re.match(r'^\d+[%s]$' % config.TIME_FILTER_METRIC_ALLOWED, time_val) is not None


_user_db = SimpleDictDBDriver(config.DATA)
_resource_db = InfluxdbDataDriver(
    coreThreadPool,
    epoch=config.RESOURCE_DATA_EPOCH,
    last=config.RESOURCE_DATA_CHUNK_DURATION,
    mean_duration=str(config.INTERVAL_SERIES_IN_SECOND) + 's')

routes_map = {
    'resources_monitoring/users/{user_id}': MonitoringGather(_user_db, _resource_db)
}
