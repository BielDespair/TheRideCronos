import sqlite3

import pandas as pd

from models.utils import get_valid_event_path
class Database:
    def __init__(self):
        self.events_path = "data/events_data/"
    
    def new_event(self, event):
        path = get_valid_event_path(self.events_path, event.name)  
        event.set_path(path)
        
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS athlete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_epc TEXT NOT NULL UNIQUE,
            plate_num TEXT NOT NULL UNIQUE
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS athlete_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id INTEGER NOT NULL,
            sended INTEGER DEFAULT 0,
            categoria TEXT NOT NULL,
            trajeto TEXT NOT NULL,
            cidade TEXT,
            patrocinador TEXT,
            BO_TemEquipe INTEGER NOT NULL,
            ID_Equipe TEXT,
            nomeAtleta TEXT NOT NULL,
            nomePlaca TEXT NOT NULL,
            numPlaca TEXT NOT NULL,
            sexo TEXT NOT NULL,
            horaLargada INTEGER,
            horaChegada INTEGER,
            gapGeral INTEGER,
            gapCategoria INTEGER,
            tempoTotal INTEGER,
            posicaoCateg INTEGER,
            posicaoGeral INTEGER,
            FOREIGN KEY (athlete_id) REFERENCES athlete(id)
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
            net_mode INTEGER,
            name TEXT,
            date TEXT,
            path TEXT,
            icon_path TEXT,
            sheet_path TEXT
        )
        ''')
    
        cursor.execute('''
            INSERT INTO event (api_id, api_token, net_mode, name, date, path, icon_path, sheet_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event.id, event.api_token, int(event.net_mode), event.name, event.date, event.event_path, event.icon_path, event.sheet_path))
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
    def query_readings(self, event_path):
        
        # Conectar ao banco de dados (ou criar um novo)
        conn = sqlite3.connect(event_path)
        cursor = conn.cursor()

        # Consulta para pegar as últimas 15 leituras com o nome do atleta
        cursor.execute('''
            SELECT 
                r.id AS reading_id,
                r.tag_epc,
                r.reading_timestamp,
                ai.nomeAtleta
            FROM 
                readings r
            JOIN 
                athlete a ON r.athlete_id = a.id
            JOIN 
                athlete_info ai ON a.id = ai.athlete_id
            ORDER BY 
                r.id DESC
            LIMIT 15
        ''')

        # Recuperar os resultados
        last_readings = cursor.fetchall()
        if not last_readings: return []

        # Exibir os resultados
        for leitura in last_readings:
            print(f'Timestamp: {leitura[0]}, Atleta: {leitura[1]}, Tag EPC: {leitura[2]}')

        # Fechar a conexão
        conn.close()
    def register_athlete(self, athlete, tag_epc, plate_num, event_path):
        
        conn = sqlite3.connect(event_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO athlete (tag_epc, plate_num) 
                VALUES (?, ?)
                ON CONFLICT(plate_num) 
                DO UPDATE SET tag_epc = excluded.tag_epc
            ''', (tag_epc, plate_num))


            # Obter o ID do atleta inserido
            athlete_id = cursor.lastrowid
            has_team = True if '-' in plate_num else False
            
            #TODO This is a temporary fix, the beicola did not answer in time
            if has_team:
                dupla = plate_num.split['-'][1]
                id_equipe = 1 if dupla == 2 else 2
            else:
                id_equipe = None
            
            # Inserir valores na tabela athlete_info (usando o athlete_id gerado)
            cursor.execute('''
                INSERT INTO athlete_info (
                    athlete_id, categoria, trajeto, cidade, patrocinador, BO_TemEquipe, ID_Equipe, 
                    nomeAtleta, nomePlaca, numPlaca, sexo
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                athlete_id, 
                athlete['Categoria'],
                athlete['Trajeto'],
                athlete['Cidade'], 
                athlete['Patrocinador'], 
                has_team,
                id_equipe,
                athlete['Nome'],
                athlete['Nome Placa'],
                athlete['Numero Placa'],
                athlete['Genero']
            ))
            # Commit para salvar as alterações no banco de dados
            conn.commit()
        except sqlite3.IntegrityError as e:
            return f"A TAG Gerou um ID duplicado. Registre-a novamente."
        finally:
            # Fechar a conexão
            conn.close()
            
    def get_registers_db(self, event_path):
        conn = sqlite3.connect(event_path)
        query = '''
        SELECT 
            a.id AS athlete_id,
            a.tag_epc,
            a.plate_num,
            ai.id AS athlete_info_id,
            ai.sended,
            ai.categoria,
            ai.trajeto,
            ai.cidade,
            ai.patrocinador,
            ai.BO_TemEquipe,
            ai.ID_Equipe,
            ai.nomeAtleta,
            ai.nomePlaca,
            ai.numPlaca,
            ai.sexo,
            ai.horaLargada,
            ai.horaChegada,
            ai.gapGeral,
            ai.gapCategoria,
            ai.tempoTotal,
            ai.posicaoCateg,
            ai.posicaoGeral
        FROM athlete AS a
        JOIN athlete_info AS ai ON a.id = ai.athlete_id
        '''
        df = pd.read_sql(query, conn)
        print(df)
        
        