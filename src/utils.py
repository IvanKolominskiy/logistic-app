from collections import namedtuple

DB_Record = namedtuple('DB_Record', [
    'name',
    'manufacture_day',
    'manufacture_month',
    'manufacture_year',
    'expiration_date',
    'expiration_year'
])


def parse_db_response(db_response: list) -> tuple:
    years = []
    equipment_records = []

    for record in db_response:
        parsed_record = DB_Record._make(record)

        years.append(parsed_record.expiration_year)

        manufacture_date = (f'{parsed_record.manufacture_day}.'
                            f'{parsed_record.manufacture_month}.'
                            f'{parsed_record.manufacture_year}')

        expiry_date = (f'{parsed_record.manufacture_day}.'
                       f'{parsed_record.manufacture_month}.'
                       f'{parsed_record.expiration_year}')

        equipment_records.append((parsed_record.name,
                                  manufacture_date,
                                  parsed_record.expiration_date,
                                  expiry_date))

    years = list(dict.fromkeys(years))
    years.append('Все')

    return years, equipment_records
