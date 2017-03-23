INTERVAL_SERIES_IN_SECOND = 2

RESOURCE_DATA_DBNAME = 'cadvisor'

RESOURCE_DATA_CHUNK_DURATION = '10m'

RESOURCE_DATA_EPOCH = 's'

# CONTROLLER_DB = {
#     'engine': 'config',
# }

# RESOURCE_MONITORING_DB = {
#     'engine': 'influxdb'
# }

DATA = {
    'users': {
        '1': {
            'machines': {
                '1': {
                    'endpoint': "localhost:3000",
                    'db': 'cadvisor'}
            }
        }
    }
}
