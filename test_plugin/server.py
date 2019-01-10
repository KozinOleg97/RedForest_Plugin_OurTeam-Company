import json
import os
from datetime import timedelta, datetime
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


class RequestHandlerBudget(web.RequestHandler):

    def initialize(self):
        self.session = db_connect_async()

    @gen.coroutine
    def get(self):
        cur_map_id = "16d23ab1-ceb1-435b-bbb5-df1b0d72aaff"

        end_date = datetime.now()
        end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        delta_date = timedelta(days=30)
        start_date = end_date - delta_date

        chart_budget_data = list()
        for cur_date in daterange(start_date, end_date):

            results = yield self.session.query(
                """SELECT data FROM budget_data 
                WHERE capture_time BETWEEN date '{date_from}' and date '{date_to}' 
                and map_id = '{map_id}' """
                    .format(
                    map_id=(cur_map_id),
                    date_from=cur_date.date(),
                    date_to=(cur_date + timedelta(days=1)).date()
                ))
            data_list = results.items()

            new_data_elem = int(0)
            for elem in data_list:
                new_data_elem += int(elem["data"] / len(data_list))

            chart_budget_data.append(new_data_elem)

            results.free()

        results.free()

        users_labels = [str(123), str(222), str(4343)]
        users_data = [1, 2, 5]
        self.render('main_page.html', title='Main Page', budget_data=chart_budget_data, users_labels=users_labels,
                    users_data=users_data)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@gen.coroutine
def update_data():
    session = db_connect_async()
    for cur_map in tracked_maps:
        data = my_plugin.company_budget(cur_map["map_id"])
        map_id = cur_map["map_id"]
        capture_time = datetime.now()

        try:
            results = yield session.query \
                ("INSERT INTO budget_data (capture_time, map_id, data) "
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
    handlers = [
        (r"/1", RequestHandlerBudget),

    ]

    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app = tornado.web.Application(handlers, **settings)

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

    print("Starting...")
    ioloop.start()
