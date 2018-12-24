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
main_map_id = "6d0d8ff3-e22d-4934-913d-5e04369ce150"


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


# полечение всех id узлов из json
def idnode_all(out):
    for item in out:
        if ((item["body"]["type_id"]) == id):
            raz(item["body"]["id"])
            global all_node
            all_node += 1
        else:
            global bad_node
            bad_node += 1
        if (item['body']['children'] != []):
            idnode_all(item['body']['children'])


# получение всей карты в json
def nodes():
    map = "63134408-5f44-441c-8c6b-799d36dc7832"
    url = "http://app.redforester.com/api/maps/" + map + "/node_types"
    out = auth_me().json()
    for item in out:
        if (item["name"] == "Задача"):
            global id
            id = item["id"]
            break

    if (id != ""):
        url = "http://app.redforester.com/api/maps/" + map + "/nodes"
        out = auth_me(url).json()
        idnode_all(out["body"]["children"])
        print(all_node, good_node, bad_node)


# из json в переменную, чтоб не писать большие условия проверки
def json_to_per(out):
    razrab = json.dumps(out["body"]["properties"]["byType"]["Разработчик"])[1:-1]
    date_start = json.dumps(out["body"]["properties"]["byType"]["Дата начала"])[1:-1]
    date_end = json.dumps(out["body"]["properties"]["byType"]["Дата окончания"])[1:-1]

    return (razrab, date_start, date_end)


# вывод только разработчиков во всех узлах
def raz(node):
    url = "http://app.redforester.com/api/nodes/" + node
    out = auth_me(url).json()
    razrab, date_start, date_end = json_to_per(out)
    if ((razrab != '') and (date_start != '') and (date_end != '')):
        print(razrab, date_start, date_end)
        global good_node
        good_node += 1


def test_req():
    url = main_url + "/api/maps/" + main_map_id
    map_dict_data = dict(get_req(auth_me(), url).json())
    name = map_dict_data["name"]
    numb_of_users = map_dict_data["user_count"]
    print("Map loaded: " + name + "\n" +
          "used by " + str(numb_of_users) + " users???????????!!!!!!!")


def company_persons(map_id):
    url = main_url + "/api/maps/" + map_id + "/users"
    users_data_list = list(get_req(auth_me(), url).json())
    print(len(users_data_list), "Users")

    for index, elem in enumerate(users_data_list):
        elem = dict(elem)
        mail = elem["username"]
        role = elem["role"]
        print(index, ") " + " User - " + mail + " role - " + role)

    pass


def company_projects_in_development(map_id):
    level = 9
    url = main_url + "/api/maps/" + map_id + "/nodes/level_count/" + str(level)
    nodes_data_dict = dict(get_req(auth_me(), url).json())

    from collections import deque
    # q = deque(nodes_data_dict["id"])

    # while q:
    #   cur_id = q.pop()
    #  body =
    #   q.append()

    pass


def ourCash(request):
    pass


def ourActivity(request):
    pass


def nodesFromThis(request):
    pass


if __name__ == '__main__':
    end_tim = 0
    start_time = time.time()

    test_req()
    company_persons(main_map_id)
    company_projects_in_development(main_map_id)

    end_tim = time.time() - start_time
print(end_tim, "sec")
