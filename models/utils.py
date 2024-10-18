import os
import shutil
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

def treat_plate_num(data):
    if '-' not in data:
        return data + '-0'
    return data


def clean_df(dataframe):
    if 'registered' in dataframe.columns: #Já foi tratado
        return
    dataframe['Numero Placa'] = dataframe['Numero Placa'].astype(str) #Transforms all Plate Num  into string
    dataframe['Numero Placa'] = dataframe['Numero Placa'].apply(treat_plate_num) #Adds a '-0' if it doenst have a hifen.
    dataframe['registered'] = False #TODO maybe the loaded sheet will already be treated and sorted...
    return dataframe
    
def sort_df(dataframe):
    dataframe[['num_part', 'suffix']] = dataframe['Numero Placa'].str.split('-', expand=True)
    dataframe['num_part'] = dataframe['num_part'].astype(int)
    dataframe['suffix'] = dataframe['suffix'].astype(int)
    dataframe = dataframe.sort_values(by=['num_part', 'suffix']).reset_index(drop=True)
    dataframe['Numero Placa'] = dataframe['num_part'].astype(str) + '-' + dataframe['suffix'].astype(str) 
    dataframe['Numero Placa'] = dataframe['Numero Placa'].str.replace(r'-0$', '', regex=True)
    dataframe['Numero Placa'] = dataframe['Numero Placa'].str.zfill(3)  # Ensure 3 digits by padding
    dataframe = dataframe.drop(columns=['num_part', 'suffix'])
    return dataframe

def import_sheet(source, destination):
    shutil.copy(source, destination)