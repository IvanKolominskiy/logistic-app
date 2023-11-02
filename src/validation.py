from datetime import datetime


def validate_manufacture_date(user_manufacture_date: str) -> str | None:
    try:
        manufacture_day, manufacture_month, manufacture_year = tuple(
            map(int, user_manufacture_date.split('.')))

        datetime(manufacture_year, manufacture_month, manufacture_day)

        if manufacture_year < 1000:
            raise ValueError

    except ValueError:
        return 'Некорректная дата производства'


def validate_shelf_life(user_expiration_date: str) -> str | None:
    try:
        int(user_expiration_date)
    except ValueError:
        return 'Некорректный срок годности'
