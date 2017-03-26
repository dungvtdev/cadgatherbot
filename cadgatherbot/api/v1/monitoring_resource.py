import falcon
from cadgatherbot.resources import coreThreadPool

import json
import re

from cadgatherbot import config
from cadgatherbot.utils.dbdriver.simpledictdb import SimpleDictDataSource
from cadgatherbot.common.data_driver import InfluxdbDataDriver

import cadgatherbot.config as config


class MonitoringController(object):

    def __init__(self, user_db, resource_db):
        self.user_db = user_db
        self.resource_db = resource_db

    def get(self, req, resp, user_id, machine_id, metric_str, **kwarg):
        last = None if 'last' not in kwarg else kwarg['last']

        metric = self.parse_metric(metric_str)
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
                                        last=last)

        data = self.post_process_resources_data(metric, result)

        resp.body = data

        return data

    def parse_metric(self, metric_str):
        # hien tai chi ho tro 1 sub partial, ex "cpu_usage_total./docker"
        if(not metric_str):
            return []

        return map(lambda x: tuple(x.strip().split('.')), metric_str.split(','))

    def post_process_resources_data(self, metric, data):
        return json.dumps(data)


class MonitoringGather(object):

    def __init__(self, user_db, resource_db):
        self.controller = MonitoringController(user_db, resource_db)

    def on_get(self, req, resp, user_id):
        if("machine" not in req.params):
            raise falcon.HTTPBadRequest(
                "Get resources monitoring need machine_id")

        machine_id = req.params['machine']
        last = None if 'last' not in req.params else req.params['last']

        if 'last' in req.params:
            last = req.params['last']
            if not re.match(r'^\d+[%s]$' % config.TIME_FILTER_METRIC_ALLOWED, last):
                raise falcon.HTTPBadRequest(
                    'The "last" params must match {number}[%s]' % config.TIME_FILTER_METRIC_ALLOWED)
        else:
            last = None

        metric = None if 'metric' not in req.params else req.params['metric']

        self.controller.get(req, resp, user_id, machine_id, metric, last=last)


_user_db = SimpleDictDataSource(config.DATA)
_resource_db = InfluxdbDataDriver(
    coreThreadPool,
    epoch=config.RESOURCE_DATA_EPOCH,
    time_filter='>' + config.RESOURCE_DATA_CHUNK_DURATION,
    time_interval=str(config.INTERVAL_SERIES_IN_SECOND) + 's')

routes_map = {
    'resources_monitoring/users/{user_id}': MonitoringGather(_user_db, _resource_db)
}
