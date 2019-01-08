from collections import Counter

import requests
import hashlib
import json
import numpy as np
import time

all_node = 0
good_node = 0
bad_node = 0
id = ""

# http://app.redforester.com/#mindmap?mapid=6d0d8ff3-e22d-4934-913d-5e04369ce150&nodeid=a35166fd-435f-4b8d-b9cb-00f5fe78e77c
main_url = "http://app.redforester.com"
# main_map_id = "6d0d8ff3-e22d-4934-913d-5e04369ce150"
main_map_id = "16d23ab1-ceb1-435b-bbb5-df1b0d72aaff";


def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


# аутинтификация пользователя
def auth_me():
    # url = "http://app.redforester.com/api/users"
    auth = ("olegkosin@rambler.ru", "b8be425b684c1dc648a6d98ad440b50c")
    # auth = ("admin@google.com", md5("verystrongpassword"))
    # auth = ("palatka199606@hotmail.com", "25a13325e8049749ba853defbc908604")
    # map = "63134408-5f44-441c-8c6b-799d36dc7832"
    # map = "6d0d8ff3-e22d-4934-913d-5e04369ce150"
    return auth


def get_req(auth, url):
    response = requests.get(url, auth=auth)
    if response.status_code != 200:
        print('Auth failed');
        raise Exception('Auth failed');
    return response


def test_req():
    url = main_url + "/api/maps/" + main_map_id
    map_dict_data = dict(get_req(auth_me(), url).json())
    name = map_dict_data["name"]
    numb_of_users = map_dict_data["user_count"]
    # print("Map loaded: " + name + "\n" +
    #      "used by " + str(numb_of_users) + " users???????????!!!!!!!")


def get_list_from_dict_tree(tree):
    from collections import deque

    res_list = []
    q = deque()
    q.append(tree)

    while q:
        cur_tree = q.pop()
        body = cur_tree["body"]
        res_list.append(body)

        children_list = body["children"]
        for node in children_list:
            q.append(node)

    return res_list


def load_tree_to_list(map_id):
    level = 9999
    url = main_url + "/api/maps/" + map_id + "/nodes/level_count/" + str(level)
    nodes_data_dict = dict(get_req(auth_me(), url).json())
    global nodes_data_list
    nodes_data_list = get_list_from_dict_tree(nodes_data_dict)


class UsersData:
    role_cnt = dict()
    number = int()

    def __init__(self, role_cnt, number):
        self.role_cnt = role_cnt
        self.number = number


def company_persons(map_id):
    url = main_url + "/api/maps/" + map_id + "/users"
    users_data_list = list(get_req(auth_me(), url).json())
    # print(len(users_data_list), "Users")
    numb = len(users_data_list)

    user_list = list()
    for index, elem in enumerate(users_data_list):
        elem = dict(elem)
        mail = elem["username"]
        role = elem["role"]
        user_list.append(role)
    # print(index, ") " + " User - " + mail + " role - " + role)
    cnt = Counter(user_list)
    res = UsersData(cnt, numb)
    return res


def get_node_type_name(type_id):
    if type_id is None:
        return None
    url = main_url + "/api/node_types/" + type_id
    node_type_info = get_req(auth_me(), url).json()
    return node_type_info["name"]


def company_projects_states(map_id):
    load_tree_to_list(map_id)
    state_list = list()
    for node in nodes_data_list:
        type_name = get_node_type_name(node["type_id"])
        if type_name == "Project":
            # print("========================================")
            # print(node["id"])
            # print(node["properties"]["global"]["title"])

            state = node["properties"]["byType"]["state"]
            state_list.append(state)

    counts = Counter(state_list)
    return counts


def company_projects_theme(map_id):
    load_tree_to_list(map_id)
    theme_list = list()
    for node in nodes_data_list:
        type_name = get_node_type_name(node["type_id"])
        if type_name == "Project":
            theme = node["properties"]["byType"]["theme"]
            theme_list.append(theme)

    counts = Counter(theme_list)
    return counts


def company_budget(map_id):
    load_tree_to_list(map_id)
    res_budget = 0
    for node in nodes_data_list:
        if "budget" in node["properties"]["byType"]:
            res_budget += int(node["properties"]["byType"]["budget"])
    return res_budget


def ourActivity(request):
    pass


def nodesFromThis(request):
    pass

# if __name__ == '__main__':
#    end_tim = 0
#    start_time = time.time()
#
#    # test_req()
#
#    users = company_persons(main_map_id)
#    states = company_projects_states(main_map_id)
#    themes = company_projects_theme(main_map_id)
#    cur_budget = company_budget(main_map_id)
#
#   end_tim = time.time() - start_time
# print(end_tim, "sec")
