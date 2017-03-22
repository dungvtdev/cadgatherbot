INTERVAL_SERIES_IN_SECOND = 2

CONTROLLER_DB = {
    'engine': 'config',
}

RESOURCE_MONITORING_DB = {
    'engine': 'influxdb'
}

DATA = {
    'users': {
        '1': {
            'machines': {
                '1': {'endpoint': "localhost:3000"}
            }
        }
    }
}
