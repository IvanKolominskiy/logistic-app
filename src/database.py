import sqlite3


def start() -> tuple:
    db = sqlite3.connect('database.db', check_same_thread=False)
    db_cursor = db.cursor()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS equipment (
        name Text UNIQUE,
        manufacture_day INTEGER,
        manufacture_month INTEGER,
        manufacture_year INTEGER,
        expiration_date INTEGER,
        expiration_year INTEGER
    )""")

    db.commit()

    return db, db_cursor


def add(db: sqlite3.Connection,
        db_cursor: sqlite3.Cursor,
        name: str,
        manufacture_day: int,
        manufacture_month: int,
        manufacture_year: int,
        expiration_date: int,
        expiration_year: int) -> None:
    db_cursor.execute(f'INSERT INTO equipment VALUES ('
                      f'"{name}", '
                      f'{manufacture_day}, '
                      f'{manufacture_month}, '
                      f'{manufacture_year}, '
                      f'{expiration_date}, '
                      f'{expiration_year})')

    db.commit()


def upload(db_cursor: sqlite3.Cursor, *parameters) -> list[tuple]:
    if parameters[0] == 'Все':
        db_cursor.execute('SELECT * FROM equipment ORDER BY expiration_year, manufacture_month, manufacture_day')
        return db_cursor.fetchall()

    expiration_year = parameters[0]

    db_cursor.execute(f'SELECT * FROM equipment\n'
                      f'WHERE expiration_year = {expiration_year}\n'
                      f'ORDER BY expiration_year, manufacture_month, manufacture_day')

    return db_cursor.fetchall()


def delete(db: sqlite3.Connection, db_cursor: sqlite3.Cursor, equipment_name: str) -> None:
    db_cursor.execute(f'DELETE FROM equipment\n'
                      f'WHERE name = "{equipment_name}"')

    db.commit()


