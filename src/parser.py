from collections import namedtuple
from typing import List, Tuple

DB_Record = namedtuple('DB_Record', [
    'record_id',
    'name',
    'manufacture_date',
    'shelf_life',
    'expiration_date'
])


def parse_db_response(db_response: List[Tuple]) -> Tuple[List, List]:
    categories = []
    equipment_records = []

    for record in db_response:
        parsed_record = DB_Record._make(record)

        categories.append(parsed_record.expiration_date.split('.')[2])

        equipment_records.append((parsed_record.record_id,
                                  parsed_record.name,
                                  parsed_record.manufacture_date,
                                  parsed_record.shelf_life,
                                  parsed_record.expiration_date))

    categories = list(dict.fromkeys(categories))
    categories.append('Ближайшее')

    return categories, equipment_records
