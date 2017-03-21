import eventlet
import json

# the pool provides a safety limit on our concurrency
pool = eventlet.GreenPool()


def app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    return "%s" % environ


if __name__ == '__main__':
    from eventlet import wsgi
    wsgi.server(eventlet.listen(('localhost', 9010)), app)
