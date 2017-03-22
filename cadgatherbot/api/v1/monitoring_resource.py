import falcon
import json

from cadgatherbot import config
from cadgatherbot.utils.dbdriver.simpledictdb import SimpleDictDataSource


class MonitoringController(object):

    def __init__(self, user_db, resource_db):
        self.user_db = user_db
        self.resource_db = resource_db

    def get(self, req, resp, user_id, machine_id, metric_str):
        metric = self.parseMetric(metric_str)
        resp.body = "heheheh"

    def parseMetric(self, metric_str):
        # hien tai chi ho tro 1 sub partial, ex "cpu_usage_total./docker"
        if(not metric_str):
            return []

        return map(lambda x: tuple(x.split('.')), metric_str.split(','))


class MonitoringGather(object):

    def __init__(self, user_db, resource_db):
        self.controller = MonitoringController(user_db, resource_db)

    def on_get(self, req, resp, user_id):
        if("machine" not in req.params):
            raise falcon.HTTPBadRequest(
                "Get resources monitoring need machine_id")

        machine_id = req.params['machine']

        if "metric" in req.params:
            metric = req.params['metric']
        else:
            metric = None

        self.controller.get(req, resp, user_id, machine_id, metric)


routes_map = {
    'resources_monitoring/users/{user_id}':
        MonitoringGather(SimpleDictDataSource(config.DATA), None),
}
