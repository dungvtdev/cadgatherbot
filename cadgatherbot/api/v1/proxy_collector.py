import falcon


class MonitoringGatherAll(object):

    def __init__(self, db_client):
        self.db_client = db_client

    def on_get(self, request, response, user_id, metric):
        # response.status = falcon.HTTP_200
        pass


routes_map = {
    'monitoring/{user_id}/{metric}': MonitoringGatherAll(None),
    'monitoring/{user_id}/machines/{machine_id}/{metric}': None
}
