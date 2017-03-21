import falcon
import eventlet
from eventlet import wsgi


class Resource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = "hehehehe"

app = falcon.API()
app.add_route("/", Resource())


def hello_world(env, start_response):
    return app(env, start_response)

wsgi.server(eventlet.listen(('', 8090)), hello_world)
