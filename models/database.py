import sqlite3
from models.utils import get_valid_event_path
class Database:
    def __init__(self):
        self.events_path = "data/events_data/"
    
    def new_event(self, event):
        id, api_token, name, date, icon_path = event.id, event.api_token, event.name, event.date, event.icon_path
        path = get_valid_event_path(self.events_path, name)  
        event.set_path(path)
        
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS event (
            path TEXT,
            id INTEGER PRIMARY KEY,
            api_token TEXT,
            name TEXT,
            date TEXT,
            icon_path TEXT
        )
        ''')
                
        # Athlete table
        cursor.execute('CREATE TABLE IF NOT EXISTS athletes (id INTEGER PRIMARY KEY, name TEXT, tag_id TEXT, plate_id TEXT)')
        #Athlete info table
        cursor.execute(' CREATE TABLE IF NOT EXISTS athlete_info (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, category TEXT, course, TEXT, birthdate DATE, phone_number TEXT, email TEXT)')
        # Updated athlete table
        cursor.execute('CREATE TABLE IF NOT EXISTS updated_athletes (id INTEGER PRIMARY KEY, prev_id TEXT, prev_tag_id TEXT, prev_category TEXT, new_id TEXT, new_tag_id TEXT, new_category TEXT)')

        # Reader data
        cursor.execute('CREATE TABLE IF NOT EXISTS reader_data (tag_id TEXT, registered_time TEXT, count INT)')
    
        cursor.execute("INSERT INTO event VALUES (?, ?, ?, ?, ?, ?)", (path, id, api_token, name, date, icon_path))
        conn.commit()
        cursor.close()
        conn.close()
            
    def query_event(self, path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM event")
            query = cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        return query