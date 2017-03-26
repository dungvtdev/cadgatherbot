import ddt
import falcon
from cadgatherbot.utils.testing import base as baseTest
import app


@ddt.ddt
class TestProxyCollectorEntry(baseTest.TestBase):

    def setUp(self):
        super(TestProxyCollectorEntry, self).setUp()
        self.api = app.app
        self.entry_path = '/api/v1/resources_monitoring'

    def test_get_return_200_when_entry_exists(self):
        path = self.entry_path + '/users/1'
        self.simulate_get(path, query_string='machine=1')
        self.assertEqual(self.srmock.status, falcon.HTTP_200)

    def test_get_return_400_when_machine_missing(self):
        path = self.entry_path + '/users/1'
        self.simulate_get(path)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)

    @ddt.data('post', 'put', 'patch', 'head')
    def test_method_not_allowed_respected(self, method):
        path = self.entry_path + '/users/1'

        getattr(self, 'simulate_' + method)(path)
        self.assertEqual(self.srmock.status, falcon.HTTP_405)

    def test_return_400_when_last_param_go_wrong(self):
        path = self.entry_path + '/users/1'
        self.simulate_get(path, query_string="machine=1&last=>123")
        self.assertRaises(falcon.HTTPBadRequest)

    def tearDown(self):
        super(TestProxyCollectorEntry, self).tearDown()
