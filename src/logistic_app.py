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
    alignment,
    dropdown,
    icons,
    colors,
)
import database
import utils


class LogisticApp(UserControl):
    def build(self):
        self.db, self.db_cursor = database.start()

        self.name_text_field = TextField(label='Наименование', width=400, border_color=colors.WHITE)
        self.manufacture_date_text_field = TextField(label='Дата изготовления', width=300, border_color=colors.WHITE)
        self.expiration_date_text_field = TextField(label='Срок годности', width=300, border_color=colors.WHITE)

        input_container = Container(
            content=Row(
                controls=[
                    self.name_text_field,
                    self.manufacture_date_text_field,
                    self.expiration_date_text_field,
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

        return Column(
            controls=[
                input_container,
                output_container,
            ],
        )

    def fill_datatable(self, e):
        db_response = database.upload(self.db_cursor, self.dropdown.value)
        _, equipment_records = utils.parse_db_response(db_response)

        self.datatable.rows = [DataRow(cells=[DataCell(Text(name),
                                                       on_double_tap=self.show_edit_display,
                                                       data=('name', record_id)),
                                              DataCell(Text(manufacture_date),
                                                       on_double_tap=self.show_edit_display,
                                                       data=('manufacture_date', record_id)),
                                              DataCell(Text(expiration_date),
                                                       on_double_tap=self.show_edit_display,
                                                       data=('expiration_date', record_id)),
                                              DataCell(Text(expiry_date)),
                                              DataCell(
                                                  IconButton(icon=icons.DELETE,
                                                             data=name,
                                                             on_click=self.delete_record)
                                              )])
                               for record_id, name, manufacture_date, expiration_date, expiry_date in equipment_records]

        self.update()

    def fill_dropdown(self, e):
        db_response = database.upload(self.db_cursor, 'Ближайшее')
        categories, _ = utils.parse_db_response(db_response)

        self.dropdown.options = [dropdown.Option(str(category)) for category in categories]

        self.update()

    def add_record(self, e):
        manufacture_day, manufacture_month, manufacture_year = tuple(
            map(int, self.manufacture_date_text_field.value.split('.')))

        expiration_date = int(self.expiration_date_text_field.value)

        expiration_year = manufacture_year + expiration_date

        database.add(self.db,
                     self.db_cursor,
                     self.name_text_field.value,
                     manufacture_day,
                     manufacture_month,
                     manufacture_year,
                     expiration_date,
                     expiration_year)

        self.name_text_field.value = ''
        self.manufacture_date_text_field.value = ''
        self.expiration_date_text_field.value = ''

        self.update()

        if self.dropdown.value == 'Ближайшее' or self.dropdown.value == str(expiration_year):
            self.fill_datatable(UserControl)

        if expiration_year not in self.dropdown.options:
            self.fill_dropdown(UserControl)

    def delete_record(self, e):
        database.delete(self.db, self.db_cursor, e.control.data)

        self.fill_datatable(UserControl)
        self.fill_dropdown(UserControl)

        self.update()

    def edit_record(self, e):
        database.update(self.db, self.db_cursor, *e.control.data, e.control.value)

        self.fill_datatable(UserControl)
        self.fill_dropdown(UserControl)

        self.update()

    def show_edit_display(self, e):
        e.control.content = TextField(bgcolor='#61677A', dense=True, on_submit=self.edit_record,
                                      data=e.control.data)

        self.update()

    def did_mount(self):
        self.fill_datatable(UserControl)
        self.fill_dropdown(UserControl)
