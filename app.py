import falcon
import cadgatherbot as api
import eventlet
from eventlet import wsgi

app = application = falcon.API()

urls_dict = api.get_urls_as_dict()
# print(urls_dict)
for route, res in urls_dict.items():
    app.add_route(route, res)

if __name__ == '__main__':
    wsgi.server(eventlet.listen(('', 8090)), app)
