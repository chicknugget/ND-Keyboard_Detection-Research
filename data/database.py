import os
import sqlite3
from data.models import Session, KeystrokeEvent, EmotionLabel, GameResult
from kivy.app import App

class DatabaseManager:

    
    def __init__(self):
        app = App.get_running_app()
        db_path = os.path.join(app.user_data_dir, 'emotion_study.db')
        self.db_path = db_path #stores database path
        self.connection = sqlite3.connect(db_path) #creates/opens a database connection  and establishes a connection to the database
        self.cursor = self.connection.cursor() #creates a cursor object for the database: basically a pen to write to the database
        self.keystroke_buffer = [] #temporary storage to store keystrokes before batch saving
        self.buffer_size = 20 #when buffer size reaches 20 --> save it all together

        self.create_tables()

    def create_tables(self):
        """create the tree tables: session, keystrokeEvent, emotionLables, gameResults"""
        
        # Sessions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                participant_id TEXT,
                start_time INTEGER,
                end_time INTEGER,
                status TEXT,
                device_model TEXT,
                android_version TEXT,
                screen_width INTEGER,
                screen_height INTEGER,
                age_range TEXT,
                gender TEXT,
                consent_time INTEGER
            )
        ''')

        # Keystroke events table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS keystroke_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                task_type TEXT,
                key_id TEXT,
                key_char TEXT,
                press_time_ms INTEGER,
                release_time_ms INTEGER,
                hold_duration_ms INTEGER,
                inter_key_interval_ms INTEGER,
                flight_time_ms INTEGER,
                touch_x REAL,
                touch_y REAL,
                key_center_x REAL,
                key_center_y REAL,
                pressure REAL,
                touch_size REAL,
                is_backspace INTEGER,
                is_error INTEGER,
                position_in_sentence INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')

        # Emotion labels table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotion_labels (
                label_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                task_type TEXT,
                selected_emoji TEXT,
                typed_sentence TEXT,
                expected_sentence TEXT,
                is_exact_match INTEGER,
                typing_duration_ms INTEGER,
                total_keystrokes INTEGER,
                backspace_count INTEGER,
                submission_time INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')

        # Game results table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                task_type TEXT,
                final_score INTEGER,
                outcome TEXT,
                start_time INTEGER,
                end_time INTEGER,
                duration_ms INTEGER,
                attempts INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        ''')
        
        # Commit the changes
        self.connection.commit()

    def insert_session(self, session):
        """Insert a new session into the database"""
        session_dict = session.to_dict()
        
        self.cursor.execute('''
            INSERT INTO sessions (
                session_id, participant_id, start_time, end_time, status,
                device_model, android_version, screen_width, screen_height,
                age_range, gender, consent_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_dict['session_id'],
            session_dict['participant_id'],
            session_dict['start_time'],
            session_dict['end_time'],
            session_dict['status'],
            session_dict['device_model'],
            session_dict['android_version'],
            session_dict['screen_width'],
            session_dict['screen_height'],
            session_dict['age_range'],
            session_dict['gender'],
            session_dict['consent_time']
        ))
        
        self.connection.commit()

    def insert_keystroke(self, keystroke):
        """Add keystroke to buffer and flush if buffer is full"""
        self.keystroke_buffer.append(keystroke)
        
        # Flush if buffer reaches specified size
        if len(self.keystroke_buffer) >= self.buffer_size:
            self.flush_keystroke_buffer()

    def flush_keystroke_buffer(self):
        """Save all buffered keystrokes to database in a single batch"""
        if not self.keystroke_buffer:
            return  # Nothing to flush
        
        # Prepare data for batch insert
        keystroke_data = []
        for keystroke in self.keystroke_buffer:
            keystroke_dict = keystroke.to_dict()
            keystroke_data.append((
                keystroke_dict['session_id'],
                keystroke_dict['task_type'],
                keystroke_dict['key_id'],
                keystroke_dict['key_char'],
                keystroke_dict['press_time_ms'],
                keystroke_dict['release_time_ms'],
                keystroke_dict['hold_duration_ms'],
                keystroke_dict['inter_key_interval_ms'],
                keystroke_dict['flight_time_ms'],
                keystroke_dict['touch_x'],
                keystroke_dict['touch_y'],
                keystroke_dict['key_center_x'],
                keystroke_dict['key_center_y'],
                keystroke_dict['pressure'],
                keystroke_dict['touch_size'],
                keystroke_dict['is_backspace'],
                keystroke_dict['is_error'],
                keystroke_dict['position_in_sentence']
            ))
        
        # Batch insert all at once
        self.cursor.executemany('''
            INSERT INTO keystroke_events (
                session_id, task_type, key_id, key_char,
                press_time_ms, release_time_ms, hold_duration_ms,
                inter_key_interval_ms, flight_time_ms,
                touch_x, touch_y, key_center_x, key_center_y,
                pressure, touch_size, is_backspace, is_error,
                position_in_sentence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', keystroke_data)
        
        self.connection.commit()
        
        # Clear buffer
        self.keystroke_buffer = []

    def insert_emotion_label(self, emotion_label):
        """Insert an emotion label into the database"""
        label_dict = emotion_label.to_dict()
        
        self.cursor.execute('''
            INSERT INTO emotion_labels (
                session_id, task_type, selected_emoji, typed_sentence,
                expected_sentence, is_exact_match, typing_duration_ms,
                total_keystrokes, backspace_count, submission_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            label_dict['session_id'],
            label_dict['task_type'],
            label_dict['selected_emoji'],
            label_dict['typed_sentence'],
            label_dict['expected_sentence'],
            label_dict['is_exact_match'],
            label_dict['typing_duration_ms'],
            label_dict['total_keystrokes'],
            label_dict['backspace_count'],
            label_dict['submission_time']
        ))
        
        self.connection.commit()

    def insert_game_result(self, game_result):
        """Insert a game result into the database"""
        result_dict = game_result.to_dict()
        
        self.cursor.execute('''
            INSERT INTO game_results (
                session_id, task_type, final_score, outcome,
                start_time, end_time, duration_ms, attempts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result_dict['session_id'],
            result_dict['task_type'],
            result_dict['final_score'],
            result_dict['outcome'],
            result_dict['start_time'],
            result_dict['end_time'],
            result_dict['duration_ms'],
            result_dict['attempts']
    ))
        
        self.connection.commit()

    def get_session(self, session_id):
        self.cursor.execute('''SELECT * FROM sessions WHERE session_id = ?''', (session_id,))
        return self.cursor.fetchone()

    def get_keystrokes(self, session_id, task_type=None):
        if task_type == None:
            self.cursor.execute('''SELECT * FROM keystroke_events WHERE session_id = ?''', (session_id,))

        else:
            self.cursor.execute('''SELECT * FROM keystroke_events WHERE session_id = ? AND task_type = ?''', (session_id, task_type,))

        return self.cursor.fetchall()

    def count_keystrokes(self, session_id):
        self.cursor.execute('''SELECT COUNT(*) FROM keystroke_events WHERE session_id = ?''', (session_id,))
        return self.cursor.fetchone()[0]

    def get_emotion_labels(self, session_id): #retrieve all emotion labels for a session
        self.cursor.execute('''SELECT * FROM emotion_labels WHERE session_id = ?''', (session_id,))
        return self.cursor.fetchall()

    def get_game_results(self, session_id):
        """Retrieve all game results for a session"""
        self.cursor.execute('''SELECT * FROM game_results WHERE session_id = ?''', (session_id,))
        return self.cursor.fetchall()
    
    def update_session(self, session_id, **kwargs):
        """Update session fields (e.g., end_time, status)"""
        valid_fields = ['end_time', 'status', 'age_range', 'gender']
        updates = []
        values = []
        for field, value in kwargs.items():
            if field in valid_fields:
                updates.append(f"{field} = ?")
                values.append(value)
        if updates:
            values.append(session_id)
            self.cursor.execute(f'''
                UPDATE sessions SET {", ".join(updates)} WHERE session_id = ?
            ''', values)
            self.connection.commit()

    def delete_session_data(self, session_id):
        """Deleting all session data when participants withdraw"""
        self.flush_keystroke_buffer()
        self.cursor.execute('DELETE FROM keystroke_events WHERE session_id = ?', (session_id,))
        self.cursor.execute('DELETE FROM emotion_labels WHERE session_id = ?', (session_id,))
        self.cursor.execute('DELETE FROM game_results WHERE session_id = ?', (session_id,))
        self.cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
        self.connection.commit()

    def close(self):
        """Close the database connection"""
        self.flush_keystroke_buffer()
        self.connection.close()
