import json
import time

sched_filename = "sched.json"

def compute_new_id(json_data):
    new_id = -1
    for key in json_data.keys():
        if(key.startswith("event_")):
            event_number = int(key.split('_')[1])
            if(event_number>new_id):
                new_id=event_number
    return new_id+1

def add_event(nota, formatted_datetime):
    with open(sched_filename, 'r') as file:
        json_data = json.load(file)
    
    latest_id = compute_new_id(json_data)
    event_key = "event_" + str(latest_id)

    if event_key not in json_data:
        json_data[event_key] = {}

    json_data[event_key]
    json_data[event_key]["nota"] = nota
    json_data[event_key]["event_datetime"] = formatted_datetime

    with open('sched.json', 'w') as file:
        json.dump(json_data, file, indent=4)

    return latest_id

def get_event_list():
    with open(sched_filename, 'r') as file:
        json_data = json.load(file)

    return json_data

def erase_event(event_id):
    with open(sched_filename, 'r') as file:
        json_data = json.load(file)

    event_key = "event_" + str(event_id)
    if event_key not in json_data:
        raise Exception("Tal evento não foi encontrado!")
    else:
        nota = json_data[event_key]["nota"]
        formatted_datetime = json_data[event_key]["event_datetime"]
        del json_data[event_key]

    with open('sched.json', 'w') as file:
        json.dump(json_data, file, indent=4)

    return nota, formatted_datetime