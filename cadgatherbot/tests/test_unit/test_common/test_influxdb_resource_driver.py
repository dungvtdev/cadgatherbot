from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_in

from cadgatherbot.common.influxdb_driver import InfluxdbDataDriver


class TestInfluxdbResources(object):

    def setUp(self):
        self.influx = InfluxdbDataDriver()

    def tearDown(self):
        del self.influx

    def test_time_filter(self):
        self.influx.setting(time_filter='>10m')
        assert_equal(self.influx._time_filter_string, 'now() > 10m')

        self.influx.setting(time_filter='>=10h')
        assert_equal(self.influx._time_filter_string, 'now() >= 10h')

        self.influx.setting(time_filter='=10s')
        assert_equal(self.influx._time_filter_string, 'now() = 10s')

    def test_query_cpu(self):
        query = self.influx.get_cpu_query(
            (('cpu1', '/'), ('cpu2', '/', '/d'), ('cpu3', )))

        assert_in('cpu1,cpu2,cpu3', query[0])
