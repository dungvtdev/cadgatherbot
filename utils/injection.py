class BaseInjectionManager(object):

    def __init__(self):
        raise CantCreateException(
            'Class InjectionManager khong the tao instance, chi dung nhu class')

    @classmethod
    def inject(cls, *argv):
        if not argv:
            return None

        list = cls.get_injection_list()
        di = tuple(map(lambda name: list[name], argv))

        return di

    @classmethod
    def get_injection_list(cls):
        raise NotImplementedError(
            'method get_injection_list of InjectionManager need implement')


class CantCreateException(Exception):
    pass
