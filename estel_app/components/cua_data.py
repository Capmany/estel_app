import reflex as rx
from estel_app.model.Cua_row import Cua_row


def cua_data(cua_row: Cua_row) -> rx.Component:
    #print(cua_row)
    return rx.heading(cua_row.estat, font_size="2em")