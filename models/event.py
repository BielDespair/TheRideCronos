
import pandas as pd
import os

from models.api import API
from models.database import Database
from models.writer import Writer
from models.event_class import Event

from models.utils import clean_df, sort_df, import_sheet

class EventModel():
    def __init__(self, event: Event):
        self.api = API()
        self.db = Database()
        self.writer = Writer()
        
        self.id = event.id
        self.api_token = event.api_token
        self.name = event.name
        self.date = event.date
        self.icon_path = event.icon_path
        self.event_path = event.event_path
        
        self.sheet_path = event.sheet_path
        self.sheet_format = '.xlsx'
        self.df = None
        self.current_index = -1
        
        self.columns = []
        self.search_key = 0
        self.event_type = None
        self.start_type = None
        
        #TODO Maybe bad code, get from a file(?)
        self.event_types = [
            "Corrida em Linha",
            "Corrida em Voltas",
            "Tempo Determinado",
            "Em Estágios",
            "Contra Relógio",
            "Revezamento",
        ]
        self.start_types = [
            "Todos",
            "Intervalo por Atleta",
            "Intervalo por Trajeto",
            "Intervalo por Categoria",
        ]
        
        self.event_categories = [
            "Elite"
        ]
        
        self.event_trajectories = [
            "Completo",
            "Reduzido"
        ]
        
    def load_df(self):
        if not self.sheet_is_present():
            return False, 0
        
        if self.sheet_format == '.xlsx':
            self.df = pd.read_excel(self.sheet_path)
        else:
            self.df = pd.read_csv(self.sheet_path)
        self.df = clean_df(self.df)
        self.df = sort_df(self.df)
        
        return True, True
        
    #Inicialization only
    def get_registered_athletes(self):
        if self.df:
            return self.df[self.df['registered'] == True]
        else:
            return []
    def register_tag(self):
        #This will write the tag epc to be the same as it TID and associate it to the athlete name/info, etc...

        self.df.loc[self.current_index, 'registered'] = True
    def get_next_athlete(self):
        if self.df is None:
            return 
        not_registered = self.df[self.df['registered'] == False]
        if not_registered.empty:
            return
        
        while True:
            self.current_index += 1
            if self.current_index >= len(self.df):
                self.current_index = 0
            if self.df['registered'].iloc[self.current_index] == False:
                return list(self.df[['Nome', 'Nome Placa', 'Numero Placa', 'Categoria']].iloc[self.current_index])
    
    def get_prev_athlete(self):
        if self.df is None:
            return
        not_registered = self.df[self.df['registered'] == False]
        if not_registered.empty:
            return
        while True:
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = len(self.df)-1
            if self.df['registered'].iloc[self.current_index] == False:
                return list(self.df[['Nome', 'Nome Placa', 'Numero Placa', 'Categoria']].iloc[self.current_index])

    def get_columns(self):
        if not self.columns:
            return ['Nome', 'Placa', 'Numero', 'Trajeto', 'Categoria']
        return self.columns
    def get_rows(self):
        if self.df is not None:
            return self.df[self.df['registered'] == False]
        else:
            return []
    def get_event_categories(self):
        return self.event_categories
    def get_event_trajectories(self):
        return self.event_trajectories
    
    def get_event_types(self):
        return self.event_types
    def get_start_types(self):
        return self.start_types
    
    def get_event_type(self):
        return self.event_type if self.event_type else ""
    def get_event_start(self):
        return self.start_type if self.start_type else ""
    def get_sheet_name(self):
        if not self.sheet_path:
            return ""
        return os.path.basename(self.sheet_path).split(".")[0]   
    
    def set_event_type(self, event_type):
        self.event_type = event_type
        #TODO: save in database
    def set_start_type(self, start_type):
        self.start_type = start_type
        #TODO: save in database
    def set_event_sheet(self, source):
        file_name = os.path.basename(source)
        path = "data/events_data/" + file_name
        import_sheet(source, path)
        self.sheet_path = path
        self.db.set_sheet_path(self.event_path, self.sheet_path)
    def sheet_is_present(self):
        if os.path.exists(str(self.sheet_path)):
                return True
        return False