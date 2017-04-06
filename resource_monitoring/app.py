from collect.collectmanager import MasterCollector
import config

import falcon
import eventlet

MasterCollector.set_config(config.collector_config)
MasterCollector.add_collector(None)
app = application = falcon.API()





