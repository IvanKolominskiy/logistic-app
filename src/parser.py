from collections import namedtuple
from typing import List, Tuple

DB_Record = namedtuple('DB_Record', [
    'record_id',
    'name',
    'manufacture_day',
    'manufacture_month',
    'manufacture_year',
    'expiration_date',
    'expiration_year'
])


def parse_db_response(db_response: List[Tuple]) -> Tuple[List, List]:
    categories = []
    equipment_records = []

    for record in db_response:
        parsed_record = DB_Record._make(record)

        categories.append(parsed_record.expiration_year)

        manufacture_date = (f'{parsed_record.manufacture_day}.'
                            f'{parsed_record.manufacture_month}.'
                            f'{parsed_record.manufacture_year}')

        expiry_date = (f'{parsed_record.manufacture_day}.'
                       f'{parsed_record.manufacture_month}.'
                       f'{parsed_record.expiration_year}')

        equipment_records.append((parsed_record.record_id,
                                  parsed_record.name,
                                  manufacture_date,
                                  parsed_record.expiration_date,
                                  expiry_date))

    categories = list(dict.fromkeys(categories))
    categories.append('Ближайшее')

    return categories, equipment_records
