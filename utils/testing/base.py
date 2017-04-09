from falcon import testing


class TestBase(testing.TestBase):

    def simulate_get(self, *args, **kwargs):
        kwargs['method'] = 'GET'
        rl = self.srmock.body = self.simulate_request(*args, **kwargs)
        return rl

    def simulate_head(self, *args, **kwargs):
        kwargs['method'] = 'HEAD'
        rl = self.srmock.body = self.simulate_request(*args, **kwargs)
        return rl

    def simulate_put(self, *args, **kwargs):
        kwargs['method'] = 'PUT'
        rl = self.srmock.body = self.simulate_request(*args, **kwargs)
        return rl

    def simulate_delete(self, *args, **kwargs):
        kwargs['method'] = 'DELETE'
        rl = self.srmock.body = self.simulate_request(*args, **kwargs)
        return rl

    def simulate_patch(self, *args, **kwargs):
        kwargs['method'] = 'PATCH'
        rl = self.srmock.body = self.simulate_request(*args, **kwargs)
        return rl

    def simulate_post(self, *args, **kwargs):
        kwargs['method'] = 'POST'
        rl = self.srmock.body = self.simulate_request(*args, **kwargs)
        return rl

    def assert_simulate_raise(self, exception_class, message_in=None):
        status = exception_class().status
        self.assertEqual(self.srmock.status, status)
        if message_in:
            # body la mot list cac string
            self.assertTrue(next((message_in in body for body in self.srmock.body), False))
