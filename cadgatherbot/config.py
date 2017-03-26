INTERVAL_SERIES_IN_SECOND = 2

RESOURCE_DATA_CHUNK_DURATION = '90s'

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
                    'endpoint': "192.168.122.76:8086",
                    'db': 'cadvisor'}
            }
        }
    }
}
