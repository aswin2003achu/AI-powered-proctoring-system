from utils.db import get_db_connection

def create_user_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        role TEXT NOT NULL,
                        image_path TEXT
                    );''')
    conn.commit()
    conn.close()
