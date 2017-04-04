import cadgatherbot.api.v1.monitoring_resource as rs
from nose.tools import assert_equal
from nose.tools import assert_true


class TestMonitoringResourceController(object):

    def setUp(self):
        self.controller = rs.MonitoringController(rs._user_db, rs._resource_db)

    def tearDown(self):
        del self.controller

    def test_parse_metric(self):
        m = ['cpu./', 'cpu./user ']
        metrics = self.controller.parse_metric(m)

        assert_equal('cpu', metrics[0][0])
        assert_true('/' == metrics[0][1] or '/user' == metrics[0][1])
