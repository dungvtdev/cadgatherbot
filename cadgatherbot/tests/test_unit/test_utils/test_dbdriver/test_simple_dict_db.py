from cadgatherbot.utils.dbdriver.simple_relationdb import SimpleDictDBDriver

from nose.tools import assert_equal
from nose.tools import assert_not_equal

DATA = {
    'users': {
        '1': {
            'machines': {
                '1': {'endpoint': "localhost:3000", }
            }
        }
    }
}


class Testdb(object):

    def setUp(self):
        self.db = SimpleDictDBDriver(DATA)

    def teardown(self):
        del self.db

    def test_cant_find_key_return_None(self):
        find = self.db.query('endpoint').key('other', '1').key('machines', '1').run()
        assert_equal(find, None)

    def test_cant_find_value_return_None(self):
        find = self.db.query().key('users', '1').key('machines', '2').run()
        assert_equal(find, None)

    def test_can_find_return_object(self):
        find = self.db.query().key('users', '1').key('machines', '1').run()
        assert_not_equal(find, None)

    def test_can_find_return_object_key(self):
        find = self.db.query('endpoint').key('users', '1').key('machines', '1').run()
        assert_equal(find['endpoint'], "localhost:3000")

    def test_cant_find_return_object_key_None(self):
        find = self.db.query('endpoint11').key('users', '1').key('machines', '1').run()
        assert_equal(find['endpoint11'], None)
