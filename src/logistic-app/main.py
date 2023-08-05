import flet
from flet import (
    Page,
    CrossAxisAlignment,
)


def main(page: Page):
    page.title = 'Logistic App'
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.bgcolor = '#D8D9DA'
    page.window_width = 1300
    page.window_height = 800
    page.update()


flet.app(target=main)
