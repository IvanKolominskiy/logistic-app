import sqlite3


def start() -> tuple:
    db = sqlite3.connect('database.db', check_same_thread=False)
    db_cursor = db.cursor()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS equipment (
        name Text,
        expiration_day INTEGER,
        expiration_month INTEGER,
        expiration_year INTEGER    
    )""")

    db.commit()

    return db, db_cursor


def add(db: sqlite3.Connection,
        db_cursor: sqlite3.Cursor,
        name: str,
        expiration_day: int,
        expiration_month: int,
        expiration_year: int) -> None:
    db_cursor.execute(f'INSERT INTO equipment VALUES ('
                      f'"{name}", '
                      f'{expiration_day}, '
                      f'{expiration_month}, '
                      f'{expiration_year})')

    db.commit()


def upload(db_cursor: sqlite3.Cursor, *parameters) -> list[tuple]:
    if parameters[0] == 'Все':
        db_cursor.execute('SELECT * FROM equipment ORDER BY expiration_year, expiration_month, expiration_day')
        return db_cursor.fetchall()

    expiration_year = parameters[0]

    db_cursor.execute(f'SELECT * FROM equipment\n'
                      f'WHERE expiration_year = {expiration_year}\n'
                      f'ORDER BY expiration_year, expiration_month, expiration_day')

    return db_cursor.fetchall()
