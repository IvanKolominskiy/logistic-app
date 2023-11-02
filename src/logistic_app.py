from flet import (
    UserControl,
    Container,
    TextField,
    TextStyle,
    Column,
    Row,
    IconButton,
    Dropdown,
    DataTable,
    DataRow,
    DataColumn,
    DataCell,
    Text,
    ListView,
    ControlEvent,
    AlertDialog,
    alignment,
    dropdown,
    icons,
    colors,
)
from typing import Type, List
from validation import validate_manufacture_date, validate_shelf_life
import database
import parser


class LogisticApp(UserControl):
    def build(self) -> Column:
        self.db, self.db_cursor = database.start()

        self.name_text_field = TextField(label='Наименование',
                                         width=400,
                                         border_color=colors.WHITE)
        self.manufacture_date_text_field = TextField(label='Дата изготовления (ДД.ММ.ГГГГ)',
                                                     width=300,
                                                     border_color=colors.WHITE)
        self.shelf_life_text_field = TextField(label='Срок годности',
                                               width=300,
                                               border_color=colors.WHITE)

        input_container = Container(
            content=Row(
                controls=[
                    self.name_text_field,
                    self.manufacture_date_text_field,
                    self.shelf_life_text_field,
                    IconButton(icon=icons.ADD_BOX, width=100, bgcolor='#61677A', on_click=self.add_record),
                ],
            ),
            bgcolor='#000000',
            border_radius=30,
            padding=30,
            margin=10,
            width=1200,
        )

        self.dropdown = Dropdown(
            width=200,
            border_color=colors.WHITE,
            value='Ближайшее',
            on_change=self.fill_datatable,
        )

        self.datatable = DataTable(
            columns=[
                DataColumn(Text("Наименование")),
                DataColumn(Text('Дата производства')),
                DataColumn(Text('Срок годности')),
                DataColumn(Text("Годен до")),
                DataColumn(Text(''))
            ],
            data_text_style=TextStyle(size=16)
        )

        list_view = ListView(expand=1, spacing=10, padding=20, controls=[self.datatable])

        output_container = Container(
            content=Row(
                controls=[
                    self.dropdown,
                    list_view,
                ],
            ),
            alignment=alignment.top_center,
            bgcolor='#61677A',
            border_radius=30,
            padding=30,
            margin=10,
            width=1200,
            height=590,
        )

        self.input_errors_dialog = AlertDialog()

        return Column(
            controls=[
                input_container,
                output_container,
                self.input_errors_dialog,
            ],
        )

    def fill_datatable(self, e: Type[UserControl]) -> None:
        db_response = database.upload(self.db_cursor, self.dropdown.value)
        _, equipment_records = parser.parse_db_response(db_response)

        self.datatable.rows = [DataRow(cells=[DataCell(Text(name),
                                                       on_double_tap=self.show_edit_display,
                                                       data=('name', (record_id, ))),
                                              DataCell(Text(manufacture_date),
                                                       on_double_tap=self.show_edit_display,
                                                       data=('manufacture_date', (record_id, shelf_life))),
                                              DataCell(Text(shelf_life),
                                                       on_double_tap=self.show_edit_display,
                                                       data=('shelf_life', (record_id, manufacture_date))),
                                              DataCell(Text(expiration_date)),
                                              DataCell(
                                                  IconButton(icon=icons.DELETE,
                                                             data=record_id,
                                                             on_click=self.delete_record)
                                              )])
                               for record_id, name, manufacture_date, shelf_life, expiration_date in equipment_records]

        self.update()

    def fill_dropdown(self, e: Type[UserControl]) -> None:
        db_response = database.upload(self.db_cursor, 'Все')
        categories, _ = parser.parse_db_response(db_response)

        self.dropdown.options = [dropdown.Option(category) for category in categories]

        self.update()

    def add_record(self, e: ControlEvent) -> None:
        errors = []

        validation_manufacture_date_error = validate_manufacture_date(self.manufacture_date_text_field.value)
        if validation_manufacture_date_error:
            errors.append(validation_manufacture_date_error)

        validation_shelf_life_error = validate_shelf_life(self.shelf_life_text_field.value)
        if validation_shelf_life_error:
            errors.append(validation_shelf_life_error)

        if errors:
            self.show_errors_display(errors)
            return

        database.add(self.db,
                     self.db_cursor,
                     self.name_text_field.value,
                     *self.manufacture_date_text_field.value.split('.'),
                     int(self.shelf_life_text_field.value))

        _, _, manufacture_year = self.manufacture_date_text_field.value.split('.')
        expiration_year = str(int(manufacture_year) + int(self.shelf_life_text_field.value))

        self.name_text_field.value = ''
        self.manufacture_date_text_field.value = ''
        self.shelf_life_text_field.value = ''

        self.update()

        if self.dropdown.value == 'Ближайшее' or self.dropdown.value == expiration_year:
            self.fill_datatable(UserControl)

        if expiration_year not in [option.key for option in self.dropdown.options]:
            self.fill_dropdown(UserControl)

    def delete_record(self, e: ControlEvent) -> None:
        database.delete(self.db, self.db_cursor, e.control.data)

        self.fill_datatable(UserControl)
        self.fill_dropdown(UserControl)

        self.update()

    def edit_record(self, e: ControlEvent) -> None:
        errors = []

        match e.control.data[0]:
            case 'manufacture_date':
                validation_manufacture_date_error = validate_manufacture_date(e.control.value)
                if validation_manufacture_date_error:
                    errors.append(validation_manufacture_date_error)
            case 'shelf_life':
                validation_shelf_life_error = validate_shelf_life(e.control.value)
                if validation_shelf_life_error:
                    errors.append(validation_shelf_life_error)

        if errors:
            self.show_errors_display(errors)
            return

        database.update(self.db, self.db_cursor, *e.control.data, e.control.value)

        self.fill_datatable(UserControl)
        self.fill_dropdown(UserControl)

        self.update()

    def show_edit_display(self, e: ControlEvent) -> None:
        e.control.content = TextField(bgcolor='#61677A', dense=True, on_submit=self.edit_record,
                                      data=e.control.data)

        self.update()

    def show_errors_display(self, errors: List[str]) -> None:
        column_controls = [Text('Обнаружены ошибки!\n', size=20)]
        column_controls.extend([Text(f'{number + 1}. {error}', size=16) for number, error in enumerate(errors)])

        self.input_errors_dialog.content = Column(
            controls=column_controls,
            height=100,
            width=300,
        )
        self.input_errors_dialog.open = True
        self.update()

    def did_mount(self) -> None:
        self.fill_datatable(UserControl)
        self.fill_dropdown(UserControl)
