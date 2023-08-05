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


class LogisticApp(UserControl):
    def build(self):
        name_text_field = TextField(label='Наименование', width=400, border_color=colors.WHITE)
        manufacture_date_text_field = TextField(label='Дата изготовления', width=300, border_color=colors.WHITE)
        expiration_date_text_field = TextField(label='Срок годности', width=300, border_color=colors.WHITE)

        input_container = Container(
            content=Row(
                controls=[
                    name_text_field,
                    manufacture_date_text_field,
                    expiration_date_text_field,
                    IconButton(icon=icons.ADD_BOX, width=100, bgcolor='#61677A'),
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
