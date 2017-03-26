from cadgatherbot.api.v1 import monitoring_resource as res

if __name__ == '__main__':
    client = res.MonitoringController(res._user_db, res._resource_db)

    req = {}

    class FakeResp():
        body = ""

    resp = FakeResp()
    user_id = '1'
    machine_id = '1'
    metric_str = 'cpu_usage_total,cpu_usage_system./docker, rx_bytes'
    # metric_str = ''
    rl = client.get(req, resp, user_id, machine_id, metric_str)

    print(rl)
