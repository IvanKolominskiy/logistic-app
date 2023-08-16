import flet
from flet import (
    Page,
    CrossAxisAlignment,
)
from logistic_app import LogisticApp


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
