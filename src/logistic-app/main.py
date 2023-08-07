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
    icons,
    colors,
)
import database


class LogisticApp(UserControl):
    def __init__(self):
        super().__init__()

        self.db_info = database.start()

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

        return Column(
            controls=[
                input_container,
            ],
        )

    def add_equipment(self, e):
        expiration_day, expiration_month, expiration_year = tuple(
            map(int, self.manufacture_date_text_field.value.split('.')))

        expiration_year += int(self.expiration_date_text_field.value)

        database.add(*self.db_info, self.name_text_field.value, expiration_day, expiration_month, expiration_year)

        self.name_text_field.value = ''
        self.manufacture_date_text_field.value = ''
        self.expiration_date_text_field.value = ''

        self.update()


def main(page: Page):
    page.title = 'Logistic App'
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.bgcolor = '#D8D9DA'
    page.window_width = 1300
    page.window_height = 800
    page.update()

    app = LogisticApp()

    page.add(app)


flet.app(target=main)
