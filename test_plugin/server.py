import tornado
import tornado.web
import test_plugin.plugin_requests as my_plugin


class Map:
    id = ""
    some_info = ""

    def __init__(self, id):
        self.id = id


class MyRequestHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("hello")
        self.finish()


def update_data():
    for cur_map in tracked_maps:
        budget = my_plugin.company_budget(cur_map.id)
        print(budget)


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'.*', MyRequestHandler),

    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()

    # periodic update every x seconds
    global tracked_maps
    tracked_maps = list()
    tracked_maps.append(Map("16d23ab1-ceb1-435b-bbb5-df1b0d72aaff"))

    task = tornado.ioloop.PeriodicCallback(update_data, 60*60*24)
    task.start()

    ioloop.start()
