import sqlite3

from models.utils import get_valid_event_path
class Database:
    def __init__(self):
        self.events_path = "data/events_data/"
    
    def new_event(self, event):
        id, api_token, name, date, icon_path, sheet_path = event.id, event.api_token, event.name, event.date, event.icon_path, event.sheet_path
        path = get_valid_event_path(self.events_path, name)  
        event.set_path(path)
        
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS athlete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag_epc TEXT NOT NULL UNIQUE,
            plate_num TEXT NOT NULL UNIQUE
        )
        ''')
                
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id INTEGER NOT NULL,
            tag_epc TEXT NOT NULL,
            reading_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (athlete_id) REFERENCES athlete(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id INTEGER NOT NULL,
            old_tag_epc TEXT NOT NULL,
            new_tag_epc TEXT NOT NULL,
            old_plate_num TEXT NOT NULL,
            new_plate_num TEXT NOT NULL,
            FOREIGN KEY (athlete_id) REFERENCES athlete(id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_id TEXT NOT NULL,
            api_token TEXT,
            name TEXT,
            date TEXT,
            path TEXT,
            icon_path TEXT,
            sheet_path TEXT
        )
        ''')
    
        cursor.execute('''
            INSERT INTO event (api_id, api_token, name, date, path, icon_path, sheet_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id, api_token, name, date, path, icon_path, sheet_path))
        conn.commit()
        cursor.close()
        conn.close()
            
    def query_event(self, path):
        # Conectar ao banco de dados
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row  # Para acessar os resultados como dicionários
        cursor = conn.cursor()
        
        try:
            # Executar a consulta
            cursor.execute("SELECT * FROM event")
            query = cursor.fetchone()  # Pegar todas as linhas
            
            # Converter para lista de dicionários
            results = dict(query)
            
        except Exception as e:
            print("Error in query event: ", e)
            results = None  # Se houver um erro, retornamos None
            
        finally:
            cursor.close()
            conn.close()
        
        return results
    def set_sheet_path(self, event_path, sheet_path):
        print(event_path)
        print(sheet_path)
        try:
            conn = sqlite3.connect(event_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE event
                SET sheet_path = ?
            ''', (sheet_path,))  # Note the comma
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
        
        
        
        