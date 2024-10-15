import pandas as pd
import os
from models.api import API
from models.database import Database
from models.event_class import Event
from models.utils import treat_plate_num
class EventModel():
    def __init__(self, event: Event):
        self.api = API()
        self.db = Database()
        
        self.id = event.id
        self.api_token = event.api_token
        self.name = event.name
        self.date = event.date
        self.icon_path = event.icon_path
        
        self.sheet = None
        self.sheet_format = '.xlsx'
        self.df = None
        self.registered_df = None

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
            self.df = pd.read_excel(self.sheet)
        else:
            self.df = pd.read_csv(self.sheet)
        self.df['Numero Placa'] = self.df['Numero Placa'].apply(treat_plate_num)
        self.df['registered'] = False
        self.sort_df()
        
        return True, True
    def sort_df(self):
        # Criar colunas auxiliares para a ordenação
        self.df['prefixo'] = self.df['Numero Placa'].str.split('-').str[0]  # Parte antes do hífen
        self.df['sufixo'] = self.df['Numero Placa'].str.split('-').str[1].fillna('0')  # Parte depois do hífen, ou 0 se não existir
        # Ordenar o DataFrame
        self.df.sort_values(by=['prefixo', 'sufixo'], ascending=[True, True], inplace=True)

        # Excluir as colunas auxiliares, se não forem necessárias
        self.df.drop(columns=['prefixo', 'sufixo'], inplace=True)
        
        self.df.to_excel('placas_ordenadas.xlsx', index=False, sheet_name='Placas Ordenadas')
    #Inicialization only
    def get_registered_athletes(self):
        if self.df:
            return self.df[self.df['registered'] == True]
        else:
            return []
    def register_athlete(self, index, tag_epc):
        #TODO save to db
        pass
    def get_next_athlete(self):
        pass

    def get_columns(self):
        if not self.columns:
            return ['Nome', 'Nome Placa', 'Numero Placa', 'Genero', 'Trajeto', 'Categoria', 'Nascimento']
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
        if not self.sheet:
            return ""
        return os.path.basename(self.sheet).split(".")[0]   
    
    def set_event_type(self, event_type):
        self.event_type = event_type
        #TODO: save in database
    def set_start_type(self, start_type):
        self.start_type = start_type
        #TODO: save in database
    def set_event_sheet(self, path):
        self.sheet = path
        #TODO: save in database
    def sheet_is_present(self):
        if not self.sheet:
            return False
        if os.path.exists(self.sheet):
                return True
        return False