import falcon
import cadgatherbot as api

app = application = falcon.API()

urls_dict = api.get_urls_as_dict()
print(urls_dict)
for route, res in urls_dict.items():
    app.add_route(route, res)
