
import pandas as pd
import os

from models.api import API
from models.database import Database
from models.writer import Writer
from models.event_class import Event

from models.utils import clean_df, sort_df, import_sheet, transform_suffix

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
        self.net_mode = event.net_mode
        
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
            "Elite",
            "Sub 35"
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

        if not 'registered' in self.df.columns:
            self.df = clean_df(self.df)
            self.df = sort_df(self.df)
        
        return True, True
        
    #Inicialization only
    def get_registered_athletes(self):
        if self.df is None: return []
        registered_rows = self.df[self.df['registered'] == True]
        if registered_rows.empty: return []
        
        return registered_rows[['Nome', 'Nome Placa', 'Numero Placa', 'Categoria']].values.tolist()
        
    def register_tag(self):
        athlete = self.df.iloc[self.current_index]
        plate_num = athlete['Numero Placa']
        error, result = self.writer.register_tag(transform_suffix(plate_num))
        if error:
            return error, result
        tag_epc = result.hex()
        error = self.db.register_athlete(athlete, tag_epc, plate_num, self.event_path)
        if error: return True, error 
        self.df.loc[self.current_index, 'registered'] = True
        self.df.to_excel(self.sheet_path)
        return False, None
    
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
            return ['Nome', 'Placa', 'Numero', 'Categoria']
        return self.columns
    def get_rows(self):
        if self.df is not None:
            return self.df[self.df['registered'] == False]
        else:
            return []
    def get_readings_rows(self):
        return self.db.query_readings(self.event_path)
    def get_event_categories(self):
        if not self.df is None:
            return self.df['Categoria'].unique()
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
        self.load_df()
        
    def sheet_is_present(self):
        if os.path.exists(str(self.sheet_path)):
                return True
        return False
    
    def add_athletes_readings(self, readings):
        print("Atletas recebidos: ", readings)
        return
        #Associate the reading tag epc with an athlete in the database
        #On START EVENT, load in memory all registered EPC on db for efficiency.......etc
        athlete_info = self.registers_df[self.registers_df_df['tag_epc'] == tag_epc]     
        # Criar um novo DataFrame a partir do novo atleta
            # Criar um dicionário com os dados do novo atleta
        novo_atleta = {
            'nomeAtleta': athlete_info['nomeAtleta'],
            'horaLargada': pd.to_datetime(athlete_info['horaLargada']),
            'horaChegada': pd.to_datetime(athlete_info['horaChegada']),
            'trajeto': athlete_info['trajeto'],
            'categoria': athlete_info['categoria']
        }
        
        new_df = pd.DataFrame([novo_atleta])
        # Concatenar o novo atleta ao DataFrame existente
        self.readings = self.readings.concat([self.readings, new_df], ignore_index=True)
        
        # Recalcular as posições
        self.calculate_placing()
        
    def calculate_placing(self):
        # Calcular o tempo total de prova
        self.readings['tempoprova'] = self.readings['horachegada'] - self.readings['horalargada']

        # Posição geral por trajeto (posGeral)
        self.readings['posGeral'] = self.readings.groupby('trajeto')['tempoprova'].rank(method='first', ascending=True)

        # Posição por categoria dentro de cada trajeto (posCategoria)
        self.readings['posCategoria'] = self.readings.groupby(['trajeto', 'categoria'])['tempoprova'].rank(method='first', ascending=True)
    def calculate_gaps(self):
        # Calcular o tempo do primeiro colocado por trajeto
        primeiro_por_trajeto = df.loc[df.groupby('trajeto')['tempoprova'].idxmin(), ['trajeto', 'tempoprova']]
        primeiro_por_trajeto.rename(columns={'tempoprova': 'tempo_primeiro'}, inplace=True)

        # Mesclar com o DataFrame original para calcular o gapGeral
        df = df.merge(primeiro_por_trajeto, on='trajeto', how='left')
        df['gapGeral'] = df['tempo_primeiro'] - df['tempoprova']

        # Calcular o tempo do primeiro colocado por categoria dentro de cada trajeto
        primeiro_por_categoria = df.loc[df.groupby(['trajeto', 'categoria'])['tempoprova'].idxmin(), ['trajeto', 'categoria', 'tempoprova']]
        primeiro_por_categoria.rename(columns={'tempoprova': 'tempo_primeiro_categoria'}, inplace=True)

        # Mesclar para calcular o gapCategoria
        df = df.merge(primeiro_por_categoria, on=['trajeto', 'categoria'], how='left')
        df['gapCategoria'] = df['tempo_primeiro_categoria'] - df['tempoprova']
        
    def initialize_readings_df(self):
        self.readings = pd.DataFrame() # For sorting posting in database. #Must contain all columns of registers
        self.readings['finished'] = False
        
    def set_athletes_start_time(self):
        #Get event config and calculate start times. Save it to db and self.readings
        #Placeholder: same time
        if self.start_type == 'Intervalo por Categoria':
            self.readings['horaLargada'] = self.readings['categoria'].map(self.start_times)
            
    def start_event(self):
        if self.net_mode == False:
            self.api.set_local()
        self.initialize_readings_df()
        self.set_athletes_start_time() #Set start time defined in the event settings (all at the same time, per category, etc...)