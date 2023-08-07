import sqlite3
from typing import Tuple


def start() -> Tuple:
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