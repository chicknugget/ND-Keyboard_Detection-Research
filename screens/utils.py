
# screens/utils.py
"""
Utility functions for participant/session ID management and data persistence
"""

import json
import time
from datetime import datetime
from pathlib import Path
import os
from kivy.app import App


# ID GENERATION

def generate_participant_id():
    """
    Generate unique participant ID
    Format: P_YYYYMMDD_HHMMSS
    Returns: str: Unique participant ID
    """
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    
    return f"P_{date_str}_{time_str}"



def generate_session_id():
    """
    Generate unique session ID for each game playthrough
    Format: SESSION_YYYYMMDD_HHMMSS_<counter>   
    Returns: str: Unique session ID
    """
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    
    # Get counter from persistent storage
    data = load_participant_data()
    counter = data.get('session_counter', 0) + 1
    
    return f"SESSION_{date_str}_{time_str}_{counter:04d}"


# DATA PERSISTENCE

def get_storage_path():
    """
    Get the path to persistent storage file
    Returns: str: Path to participant_data.json
    """
    app = App.get_running_app()
    if app:
        # Use Kivy's user_data_dir for persistent storage
        storage_dir = app.user_data_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        return os.path.join(storage_dir, 'participant_data.json')
    return 'participant_data.json'


def load_participant_data():
    """
    Load participant data from persistent storage
    """
    storage_path = get_storage_path()
    
    try:
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                data = json.load(f)
                print(f" Loaded participant data from {storage_path}")
                return data
        else:
            print(f" No existing participant data found at {storage_path}")
            return {}
    except Exception as e:
        print(f" Error loading participant data: {e}")
        return {}


def save_participant_data(data):
    """
    Save participant data to persistent storage
    """
    storage_path = get_storage_path()
    
    try:
        with open(storage_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f" Saved participant data to {storage_path}")
        return True
    except Exception as e:
        print(f" Error saving participant data: {e}")
        return False


def get_or_create_participant_id():
    """
    Get existing participant ID or create new one
    """
    data = load_participant_data()
    
    if 'participant_id' in data and data['participant_id']:
        print(f" Retrieved existing participant ID: {data['participant_id']}")
        return data['participant_id'], False
    else:
        new_id = generate_participant_id()
        data['participant_id'] = new_id
        data['participant_counter'] = data.get('participant_counter', 0) + 1
        data['created_at'] = time.time()
        data['total_sessions'] = 0
        save_participant_data(data)
        print(f" Created new participant ID: {new_id}")
        return new_id, True


def increment_session_count():
    """
    Increment the total session count and session counter in participant data
    """
    data = load_participant_data()
    data['total_sessions'] = data.get('total_sessions', 0) + 1
    data['session_counter'] = data.get('session_counter', 0) + 1
    save_participant_data(data)
    return data['total_sessions']


def clear_participant_data():
    """
    Clear all participant data (used on Reset)
    """
    storage_path = get_storage_path()
    
    try:
        if os.path.exists(storage_path):
            os.remove(storage_path)
            print(f" Cleared participant data from {storage_path}")
        else:
            print(f" No participant data to clear")
        return True
    except Exception as e:
        print(f" Error clearing participant data: {e}")
        return False


# APP DATA HELPERS

def init_app_data():
    """
    Initialize app data structure
    """
    participant_id, is_new = get_or_create_participant_id()
    
    return {
        'participant_id': participant_id,
        'is_first_time': is_new,
        'session_id': None,  # Generated when starting game
        'current_game': 0,   # 0-6 (7 games total)
        'demographics': {},
        'tasks': [],         # List of completed tasks
        'debriefing_complete': False,
        'session_counter': 0  # Initialize session counter
    }


def reset_app_data():
    """
    Reset all app data and clear participant ID
    """
    clear_participant_data()
    new_data = init_app_data()
    print(" App data reset - new participant created")
    return new_data


def get_backend_data():
    """
    Get all collected data formatted for backend submission
    Returns:
        dict:{}
    """
    app = App.get_running_app()
    
    if not app:
        return {}
    
    return {
        'participant_id': app.user_data.get('participant_id', ''),
        'session_id': app.user_data.get('session_id', ''),
        'session_start_time': app.user_data.get('session_start_time', ''),
        'session_end_time': app.user_data.get('session_end_time', ''),
        'level': app.user_data.get('tasks', [])
    }