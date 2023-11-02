import sqlite3
from typing import List, Tuple


def start() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db = sqlite3.connect('../data/database.db', check_same_thread=False)
    db_cursor = db.cursor()

    db_cursor.execute("""CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY,
        name TEXT,
        manufacture_date TEXT,
        shelf_life INTEGER,
        expiration_date TEXT
    )""")

    db.commit()

    return db, db_cursor


def add(db: sqlite3.Connection,
        db_cursor: sqlite3.Cursor,
        name: str,
        manufacture_day: str,
        manufacture_month: str,
        manufacture_year: str,
        shelf_life: int) -> None:
    db_cursor.execute(f'INSERT INTO equipment (name, manufacture_date, shelf_life, expiration_date) VALUES\n'
                      f'("{name}", '
                      f'DATE("{manufacture_year}-{manufacture_month}-{manufacture_day}"), '
                      f'{shelf_life}, '
                      f'DATE("{manufacture_year}-{manufacture_month}-{manufacture_day}", "{shelf_life} years"))')

    db.commit()


def upload(db_cursor: sqlite3.Cursor, category: str) -> List[Tuple[str, str, str]]:
    match category:
        case 'Все':
            db_cursor.execute('SELECT '
                              'id, '
                              'name, '
                              'strftime("%d.%m.%Y", manufacture_date), '
                              'shelf_life, '
                              'strftime("%d.%m.%Y", expiration_date) FROM equipment\n'
                              'ORDER BY expiration_date')
            return db_cursor.fetchall()

        case 'Ближайшее':
            db_cursor.execute('SELECT '
                              'id, '
                              'name, '
                              'strftime("%d.%m.%Y", manufacture_date), '
                              'shelf_life, '
                              'strftime("%d.%m.%Y", expiration_date) FROM equipment\n'
                              'WHERE expiration_date >= DATE("now")\n'
                              'ORDER BY expiration_date')
            return db_cursor.fetchall()

        case expiration_year:
            db_cursor.execute(f'SELECT '
                              f'id, '
                              f'name, '
                              f'strftime("%d.%m.%Y", manufacture_date), '
                              f'shelf_life, '
                              f'strftime("%d.%m.%Y", expiration_date) FROM equipment\n'
                              f'WHERE expiration_date BETWEEN "{expiration_year}-01-01" AND "{expiration_year}-12-31"\n'
                              f'ORDER BY expiration_date')

            return db_cursor.fetchall()


def delete(db: sqlite3.Connection, db_cursor: sqlite3.Cursor, record_id: str) -> None:
    db_cursor.execute(f'DELETE FROM equipment\n'
                      f'WHERE id = "{record_id}"')

    db.commit()


def update(db: sqlite3.Connection,
           db_cursor: sqlite3.Cursor,
           column: str,
           update_data: int,
           new_value: int | str) -> None:
    match column:
        case 'name':
            record_id = update_data

            db_cursor.execute(f'UPDATE equipment\n'
                              f'SET {column} = "{new_value}"\n'
                              f'WHERE id = {record_id}')
        case 'manufacture_date':
            record_id, shelf_life = update_data
            manufacture_day, manufacture_month, manufacture_year = new_value.split('.')

            db_cursor.execute(f'UPDATE equipment\n'
                              f'SET {column} = DATE("{manufacture_year}-{manufacture_month}-{manufacture_day}"),\n'
                              f'    expiration_date = DATE("{manufacture_year}-{manufacture_month}-{manufacture_day}", '
                              f'                            "{shelf_life} years")\n'
                              f'WHERE id = {record_id}')
        case 'shelf_life':
            record_id, manufacture_date = update_data
            manufacture_day, manufacture_month, manufacture_year = manufacture_date.split('.')

            db_cursor.execute(f'UPDATE equipment\n'
                              f'SET {column} = {new_value},\n'
                              f'    expiration_date = DATE("{manufacture_year}-{manufacture_month}-{manufacture_day}", '
                              f'                            "{new_value} years")\n'
                              f'WHERE id = {record_id}')

    db.commit()
