from api.v1 import proxy_collector as proxy_collector_v1
from exceptions import *


def populateResource(url_dict, prefix_version, resource):
    routes_map = resource.routes_map
    if(not routes_map):
        raise APIInternalError("API version {version} not found".format(
            version=prefix_version))

    for route, res in routes_map.items():
        url_dict[prefix_version + route] = res


def create_urls():
    url_dict = {}

    # v1
    v1 = '/api/v1/'
    populateResource(url_dict, v1, proxy_collector_v1)

    return url_dict
