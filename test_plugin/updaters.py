import test_plugin.plugin_requests as my_plugin
import queries


async def update_budget(cur_map, session, capture_time):
    budget_data = my_plugin.company_budget(cur_map["map_id"])
    map_id = cur_map["map_id"]

    try:
        results = await session.query \
            ("INSERT INTO budget_data (capture_time, map_id, data) "
             "VALUES (%s, %s, %s)",
             [capture_time,
              map_id,
              budget_data])
        results.free()
    except (queries.DataError,
            queries.IntegrityError) as error:
        print("db error")
    print("budget_data write for map " + (cur_map["map_id"]) + " data = " + str(budget_data))


async def update_users(cur_map, session, capture_time):
    users_data = my_plugin.company_persons(cur_map["map_id"])
    map_id = cur_map["map_id"]

    try:
        results = await session.query \
            ("""INSERT INTO users_data (capture_time, map_id, role_names, role_numbers, number)
                    VALUES (%s, %s, %s, %s, %s)""",
             [capture_time,
              map_id,
              list(users_data.role_cnt.keys()),
              list(users_data.role_cnt.values()),
              users_data.number
              ])
        results.free()
    except (queries.DataError,
            queries.IntegrityError) as error:
        print("db error")

    print(
        "users_data write for map " + cur_map["map_id"] + " data = " + ''.join(
            str(e) + "; " for e in users_data.role_cnt) +
        " " + str(users_data.number))


async def update_states(cur_map, session, capture_time):
    states_data = my_plugin.company_projects_states(cur_map["map_id"])
    map_id = cur_map["map_id"]
    try:
        results = await session.query \
            ("""INSERT INTO states_data (capture_time, map_id, status_names, status_numbers, number)
                            VALUES (%s, %s, %s, %s, %s)""",
             [capture_time,
              map_id,
              list(states_data.states_cnt.keys()),
              list(states_data.states_cnt.values()),
              states_data.number
              ])
        results.free()
    except (queries.DataError,
            queries.IntegrityError) as error:
        print("db error")

    print(
        "states_data write for map " + cur_map[
            "map_id"] + " data = " + ''.join(str(e) + "; " for e in states_data.states_cnt) + " " + str(
            states_data.number))
