def parse_db_response(db_response: list) -> tuple:
    years = []
    equipment_record = []

    for record in db_response:
        name, expiration_day, expiration_month, expiration_year = record

        years.append(expiration_year)
        equipment_record.append((name, f'{expiration_day}.{expiration_month}.{expiration_year}'))

    return list(dict.fromkeys(years)), equipment_record

