import os
import shutil
import re
import time

events_path = "data/events_data/"


def create_event_path(name):
    path = events_path + name
    if os.path.exists(path):
        count = 0
        for file in os.listdir(path):
            if os.path.exists(path):
                count += 1
        path = path+"_"+str(count)
    print("Final Path:", path)
    os.mkdir(path)
    return path
def delete_event_path(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def get_events_paths():
    events = []
    for file in os.listdir(events_path):
        events.append(events_path + file)
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
    dataframe['Numero Placa'] = dataframe['Numero Placa'].astype(str) #Transforms all Plate Num  into string
    dataframe['Numero Placa'] = dataframe['Numero Placa'].apply(treat_plate_num) #Adds a '-0' if it doenst have a hifen.
    dataframe['registered'] = False #TODO maybe the loaded sheet will already be treated and sorted...
    dataframe['tag_epc'] = ""
    dataframe.rename(columns={'Assessoria / Equipe': 'Patrocinador'}, inplace=True)
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
    
    
def transform_suffix(suffix):
    # Verifica se o formato é xxx-y
    if '-' in suffix:
        # Divide a string pelo '-'
        parts = suffix.split('-')
        return parts[0] + parts[1]
    
    # Se a string termina com um único dígito
    elif len(suffix) == 3 and suffix[-1].isdigit():
        return suffix + '0'
    
    # Retorna a string original se nenhuma condição for atendida
    return suffix