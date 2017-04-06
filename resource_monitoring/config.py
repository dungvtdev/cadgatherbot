collector_config = {
    'duration': 60,
    'query_pattern': "{endpoint}/api/v1/resources_monitoring/users/{user_id}?machine={machine_id}",
    'collected_metrics': ['cpu_usage_total./', 'rx_bytes'],
    'backward_time': 120,
}
