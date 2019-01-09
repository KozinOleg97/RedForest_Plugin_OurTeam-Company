from datetime import datetime
import pprint

import tornado
from tornado import gen, ioloop, web
import test_plugin.plugin_requests as my_plugin
import queries


def db_connect_async():
    db_uti = queries.uri("localhost", 5432, "plugin_db", "postgres", "postgres")
    return queries.TornadoSession(db_uti)


def db_connect_sync():
    db_uti = queries.uri("localhost", 5432, "plugin_db", "postgres", "postgres")
    return queries.Session(db_uti)


class Map:
    id = ""
    some_info = ""

    def __init__(self, id):
        self.id = id


class MyRequestHandler(web.RequestHandler):

    def initialize(self):
        self.session = db_connect_async()

    @gen.coroutine
    def get(self):
        results = yield self.session.query('SELECT map_id FROM maps')
        for row in results:
            self.write(row)
        self.finish("\n end!")
        results.free()


@gen.coroutine
def update_data():
    session = db_connect_async()
    for cur_map in tracked_maps:
        data = my_plugin.company_budget(cur_map["map_id"])
        map_id = cur_map["map_id"]
        capture_time = datetime.now()

        try:
            results = yield session.query("INSERT INTO budget_data (Сapture_time, map_id, data) "
                                          "VALUES (%s, %s, %s)",
                                          [capture_time,
                                           map_id,
                                           data])
            results.free()
        except (queries.DataError,
                queries.IntegrityError) as error:
            print("db error")

        print(data)


def init_server():
    session = db_connect_sync()
    results = session.query('SELECT map_id FROM maps')

    res = results.items()
    return res


if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/1", MyRequestHandler),

    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()

    global tracked_maps
    tracked_maps = list()
    tracked_maps = init_server()
    pass
    # periodic update every x ms

    task = tornado.ioloop.PeriodicCallback(update_data, 1000 * 20)  # 1000 * 60 * 60 * 24)
    task.start()

    ioloop.start()
