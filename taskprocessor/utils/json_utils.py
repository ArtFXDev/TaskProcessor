import io
import json


def json_to_dict(json_data):
    task_dict = None
    if type(json_data) is str:
        task_dict = json.loads(json_data)
    elif type(json_data) is io.TextIOWrapper:
        task_dict = json.load(json_data)

    return task_dict


def dict_to_json(dict_data):
    return json.dumps(dict_data)
