import sqlite3

def get_connection():
    return sqlite3.connect("data.db")


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_table()
    print("Table created successfully.")