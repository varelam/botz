import json
import os
import datetime

sched_filename = "sched.json"

def get_night_message():
    json_data = get_event_list()
    date_format = "%d-%m"
    current_year = datetime.datetime.now().year
    message = ""
    for event_str, event in json_data.items():
        event_number = -1
        if(event_str.startswith("event_")):
            event_number = int(event_str.split('_')[1])
            nota = event["nota"]
            formatted_datetime = event["event_datetime"]
            date_obj = datetime.datetime.strptime(formatted_datetime, date_format)
            date_obj = date_obj.replace(year=current_year)
            current_time = datetime.datetime.now()
            time_difference = (date_obj - current_time)
            if 0 <= time_difference.days < 1:
                message = message + "Nota **{}**: **\"{}\"**, no dia **{}**\n".format(event_number,nota,formatted_datetime)

    if len(message):
        message = "Boas! Não esquecer o que há para fazer amanhã!\n" + message + "\nBons soninhos!"
    else:
        message = "Boas! Hoje não há eventos para amanhã!"

    return message

def compute_new_id(json_data):
    new_id = -1
    for key in json_data.keys():
        if(key.startswith("event_")):
            event_number = int(key.split('_')[1])
            if(event_number>new_id):
                new_id=event_number
    return new_id+1

def add_event(nota, formatted_datetime):
    if not os.path.exists(sched_filename):
        with open(sched_filename, 'w') as file:
            file.write('{}')

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