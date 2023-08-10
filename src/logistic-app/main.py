import flet
from flet import (
    Page,
    CrossAxisAlignment,
    UserControl,
    Container,
    TextField,
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
    def __init__(self):
        super().__init__()

        self.db, self.db_cursor = database.start()

        db_response = database.upload(self.db_cursor, 'all')
        years, equipment_records = utils.parse_db_response(db_response)

        years.append('Ближайшее')

        self.year_dropdown_options = [dropdown.Option(str(year)) for year in years]

        self.equipment_datatable_rows = [DataRow(cells=[DataCell(Text(name)), DataCell(Text(expiration_date))])
                                         for name, expiration_date in equipment_records]

        self.name_text_field = TextField(label='Наименование', width=400, border_color=colors.WHITE)
        self.manufacture_date_text_field = TextField(label='Дата изготовления', width=300, border_color=colors.WHITE)
        self.expiration_date_text_field = TextField(label='Срок годности', width=300, border_color=colors.WHITE)

    def build(self):
        input_container = Container(
            content=Row(
                controls=[
                    self.name_text_field,
                    self.manufacture_date_text_field,
                    self.expiration_date_text_field,
                    IconButton(icon=icons.ADD_BOX, width=100, bgcolor='#61677A', on_click=self.add_equipment),
                ],
            ),
            bgcolor='#000000',
            border_radius=10,
            padding=30,
            margin=10,
            width=1200,
        )

        list_view = ListView(expand=1, spacing=10, padding=20)

        list_view.controls.append(
            DataTable(
                columns=[
                    DataColumn(Text("Наименование")),
                    DataColumn(Text("Годен до")),
                ],
                rows=self.equipment_datatable_rows,
            ),
        )

        output_container = Container(
            content=Row(
                controls=[
                    Dropdown(
                        width=300,
                        options=self.year_dropdown_options,
                        border_color=colors.WHITE,
                        value='Ближайшее'
                    ),
                    list_view,
                ],
            ),
            alignment=alignment.top_center,
            bgcolor='#61677A',
            border_radius=10,
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

    def add_equipment(self, e):
        expiration_day, expiration_month, expiration_year = tuple(
            map(int, self.manufacture_date_text_field.value.split('.')))

        expiration_year += int(self.expiration_date_text_field.value)

        database.add(self.db,
                     self.db_cursor,
                     self.name_text_field.value,
                     expiration_day,
                     expiration_month,
                     expiration_year)

        self.name_text_field.value = ''
        self.manufacture_date_text_field.value = ''
        self.expiration_date_text_field.value = ''

        self.update()


def main(page: Page):
    page.title = 'Logistic App'
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.bgcolor = '#D8D9DA'
    page.window_width = 1300
    page.window_height = 810
    page.update()

    app = LogisticApp()

    page.add(app)


flet.app(target=main)
