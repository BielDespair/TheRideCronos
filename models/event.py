import pandas as pd
class EventModel():
    def __init__(self):
        self.sheet_path = None
        self.sheet_format = '.xlsx'
        self.df = None
        self.columns = []
        self.search_key = 0
        
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
        return [[1,2,3,4,5,6,7] for _ in range(100)]
    
    def get_event_types(self):
        return self.event_types
    def get_start_types(self):
        return self.start_types
