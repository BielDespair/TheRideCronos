import pandas as pd
import os
from models.api import API
from models.event_class import Event
class EventModel():
    def __init__(self, event: Event):
        self.api = API()
        
        self.id = event.id
        self.api_token = event.api_token
        self.name = event.name
        self.date = event.date
        self.icon_path = event.icon_path
        
        self.sheet_path = None
        self.sheet_format = '.xlsx'
        self.df = None
        self.columns = []
        self.search_key = 0
        self.event_type = None
        self.start_type = None
        
        #Atributos da Prova
        self.teams = 0
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
        

    def load_df(self):
        if self.sheet_format == '.xlsx':
            data = pd.read_excel(self.sheet_path)
        else:
            data = pd.read_csv(self.sheet_path)
        
    def next_register(self):
        pass
    
    def get_columns(self):
        if not self.columns:
            return ['Nome', 'Placa', 'Número', 'Gênero', 'Trajeto', 'Categoria', 'Idade']
        return self.columns
    def get_rows(self):
        if self.df:
            return self.df.to_dict('records')
        return [[1,2,3,4,5,6,7] for _ in range(1)]
    
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
        return os.path.basename(self.sheet_path)
    
    def set_event_type(self, event_type):
        self.event_type = event_type
        #TODO: save in database
    def set_start_type(self, start_type):
        self.start_type = start_type
        #TODO: save in database
    def sheet_is_present(self):
        if not self.sheet_path:
            return False
        if os.path.exists(self.sheet_path):
            return True
        return False
        
    