INTERVAL_SERIES_IN_SECOND = 2

RESOURCE_DATA_CHUNK_DURATION = '90s'

RESOURCE_DATA_EPOCH = 's'

TIME_FILTER_METRIC_ALLOWED = 'smhd'
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
                    'endpoint': "192.168.122.121:8086",
                    'db': 'cadvisor'}
            }
        }
    }
}
