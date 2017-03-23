import eventlet
from eventlet.green import urllib2


urls = [
    "http://www.google.com/intl/en_ALL/images/logo.gif",
    "https://wiki.secondlife.com/w/images/secondlife.jpg",
    "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
]


def fetch(url):
    return urllib2.urlopen(url).read()


pool = eventlet.GreenPool()

for body in pool.imap(fetch, urls):
    print("got body", len(body))
