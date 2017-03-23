class BaseResourcesDataDriver(object):
    protocol = None

    def __init__(self, **kwargv):
        self.setting(**kwargv)

    def setting(self, **kwargv):
        if 'protocol' in kwargv:
            self.protocol = kwargv['protocol']

    def query(endpoint, db_name, metric):
        raise NotImplementedError(
            'Method query of BaseInfluxdb must be inplemented')

    def protocol_decorate(self, endpoint):
        p = self.protocol or "http"
        return p + "://" + endpoint
