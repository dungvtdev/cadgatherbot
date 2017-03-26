from cadgatherbot.utils.injection import BaseInjectionManager
from . import resources


class InjectionManager(BaseInjectionManager):

    @classmethod
    def get_injection_list(cls):
        list = {
            'CORE_THREAD_POOL': resources.coreThreadPool
        }

        return list
