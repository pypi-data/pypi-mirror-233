import json


def load_json(path):
    with open(path) as file:
        payload = file.read()
    return json.loads(payload)


def write_json(path, data):
    with open(path, "w") as json_file:
        json.dump(data, json_file)
