import os

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