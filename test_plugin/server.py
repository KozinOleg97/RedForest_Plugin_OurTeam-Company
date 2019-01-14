import json
import os
from datetime import timedelta, datetime
import pprint

import tornado
from tornado import gen, ioloop, web
import test_plugin.plugin_requests as my_plugin
import queries

from test_plugin.updaters import *


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

    async def get(self):
        print("start")
        cur_map_id = "16d23ab1-ceb1-435b-bbb5-df1b0d72aaff"

        end_date = datetime.now()
        end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        delta_date = timedelta(days=30)
        start_date = end_date - delta_date

        chart_budget_data = list()
        users_numbers_list = list()
        states_numbers_list = list()
        for cur_date in daterange(start_date, end_date):

            # ======== budget =======================================================================================
            results = await self.session.query(
                """SELECT data FROM budget_data 
                WHERE capture_time BETWEEN date '{date_from}' and date '{date_to}' 
                and map_id = '{map_id}' """
                    .format(
                    map_id=(cur_map_id),
                    date_from=cur_date.date(),
                    date_to=(cur_date + timedelta(days=1)).date()
                ))
            budget_data_list = results.items()

            new_data_elem = int(0)
            for elem in budget_data_list:
                new_data_elem += int(elem["data"] / len(budget_data_list))

            chart_budget_data.append(new_data_elem)
            results.free()

            # ========== users ======================================================================================
            results = await self.session.query(
                """SELECT role_names, role_numbers, number FROM users_data 
                WHERE capture_time BETWEEN date '{date_from}' and date '{date_to}' 
                and map_id = '{map_id}' """
                    .format(
                    map_id=(cur_map_id),
                    date_from=cur_date.date(),
                    date_to=(cur_date + timedelta(days=1)).date()
                ))  # TODO there might appear multiple records of users, so need check this out or don't let this happen

            users_data_list = results.items()
            if len(users_data_list) != 0:
                users_numbers_list.append(users_data_list[len(users_data_list) - 1]["number"])
            else:
                users_numbers_list.append(int(0))
            results.free()

            # ========== project_states ===================================================================================
            results = await self.session.query(
                """SELECT status_names, status_numbers, number FROM states_data 
                WHERE capture_time BETWEEN date '{date_from}' and date '{date_to}' 
                and map_id = '{map_id}' """
                    .format(
                    map_id=(cur_map_id),
                    date_from=cur_date.date(),
                    date_to=(cur_date + timedelta(days=1)).date()
                ))  # TODO there might appear multiple records of users, so need check this out or don't let this happen

            states_data_list = results.items()
            if len(states_data_list) != 0:
                states_numbers_list.append(states_data_list[len(states_data_list) - 1]["number"])
            else:
                states_numbers_list.append(int(0))
            results.free()

        cur_states_data = await my_plugin.company_projects_states(cur_map_id)
        states_labels = list(cur_states_data.states_cnt.keys())
        states_data = list(cur_states_data.states_cnt.values())

        if len(states_data_list) != 0:
            states_labels = states_data_list[len(states_data_list) - 1]["status_names"]
            states_data = states_data_list[len(states_data_list) - 1]["status_numbers"]

        if len(users_data_list) != 0:
            users_labels = users_data_list[len(users_data_list) - 1]["role_names"]
            users_data = users_data_list[len(users_data_list) - 1]["role_numbers"]

        print("end")
        self.render('main_page.html', title='Main Page', budget_data=chart_budget_data, users_labels=users_labels,
                    users_data=users_data, users_numbers=users_numbers_list, states_labels=states_labels,
                    states_data=states_data)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


async def update_data():
    print("================ New update ======================")
    session = db_connect_async()
    capture_time = datetime.now()
    for cur_map in tracked_maps:
        await update_budget(cur_map, session, capture_time)

        await update_users(cur_map, session, capture_time)

        await update_states(cur_map, session, capture_time)


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

    task = tornado.ioloop.PeriodicCallback(update_data, 1000 * 120)  # 1000 * 60 * 60 * 24)
    task.start()

    print("Starting...")
    ioloop.start()
