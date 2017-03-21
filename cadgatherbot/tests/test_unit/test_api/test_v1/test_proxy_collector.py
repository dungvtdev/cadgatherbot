import ddt
import falcon
from utils.testing import base as baseTest
import app


@ddt.ddt
class TestProxyCollectorEntry(baseTest.TestBase):

    def setUp(self):
        super(TestProxyCollectorEntry, self).setUp()
        self.api = app.app
        self.entry_path = '/api/v1/monitoring'

    def test_get_return_200_when_entry_exists(self):
        path = self.entry_path + '/1/cpu_usage_total'
        self.simulate_get(path)
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    @ddt.data('post', 'put', 'patch', 'head')
    def test_method_not_allowed_respected(self, method):
        path = self.entry_path + '/1/cpu_usage_total'

        getattr(self, 'simulate_' + method)(path)
        self.assertEqual(self.srmock.status, falcon.HTTP_405)

    def tearDown(self):
        super(TestProxyCollectorEntry, self).tearDown()
