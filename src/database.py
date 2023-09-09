import sqlite3


def start() -> tuple:
    db = sqlite3.connect('../data/database.db', check_same_thread=False)
    db_cursor = db.cursor()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY,
        name Text,
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
    db_cursor.execute(f'INSERT INTO equipment '
                      f'(name, manufacture_day, manufacture_month, manufacture_year, expiration_date, expiration_year) '
                      f'VALUES ('
                      f'"{name}", '
                      f'{manufacture_day}, '
                      f'{manufacture_month}, '
                      f'{manufacture_year}, '
                      f'{expiration_date}, '
                      f'{expiration_year})')

    db.commit()


def upload(db_cursor: sqlite3.Cursor, category: int | str) -> list[tuple]:
    if category == 'Все':
        db_cursor.execute('SELECT * FROM equipment ORDER BY expiration_year, manufacture_month, manufacture_day')
        return db_cursor.fetchall()

    expiration_year = category

    db_cursor.execute(f'SELECT * FROM equipment\n'
                      f'WHERE expiration_year = {expiration_year}\n'
                      f'ORDER BY expiration_year, manufacture_month, manufacture_day')

    return db_cursor.fetchall()


def delete(db: sqlite3.Connection, db_cursor: sqlite3.Cursor, equipment_name: str) -> None:
    db_cursor.execute(f'DELETE FROM equipment\n'
                      f'WHERE name = "{equipment_name}"')

    db.commit()


def update(db: sqlite3.Connection,
           db_cursor: sqlite3.Cursor,
           column: str,
           record_id: int,
           new_value: int | str) -> None:
    match column:
        case 'name':
            db_cursor.execute(f'UPDATE equipment\n'
                              f'SET {column} = "{new_value}"\n'
                              f'WHERE id = {record_id}')
        case 'manufacture_date':
            manufacture_day, manufacture_month, manufacture_year = new_value.split('.')

            db_cursor.execute(f'UPDATE equipment\n'
                              f'SET manufacture_day = {manufacture_day},\n'
                              f'    manufacture_month = {manufacture_month},\n'
                              f'    manufacture_year = {manufacture_year},\n'
                              f'    expiration_year = {manufacture_year} + expiration_date\n'
                              f'WHERE id = {record_id}')
        case 'expiration_date':
            db_cursor.execute(f'UPDATE equipment\n'
                              f'SET {column} = {new_value},\n'
                              f'    expiration_year = manufacture_year + {new_value}\n'
                              f'WHERE id = {record_id}')

    db.commit()
