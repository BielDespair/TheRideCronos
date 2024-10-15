import os
import re

def get_valid_event_path(path, name):
    final_path = path+name+".db"
    if os.path.exists(path+name+".db"):
        count = 0
        for file in os.listdir(path):
            if file.startswith(name):
                count += 1
        final_path = path+name+str(count)+".db"
    return final_path

def get_events_paths(path):
    events = []
    for file in os.listdir(path):
        if file.endswith(".db"):
            events.append(path+file)
    return events

def format_date_of_birth(date):
    date = re.sub(r'\D', '', data)
    if len(data) > 8:
        data = data[:8]
    if len(data) > 2:
        data = data[:2] + '/' + data[2:]
    if len(data) > 5:
        data = data[:5] + '/' + data[5:9]
    return date