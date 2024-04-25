import reflex as rx

from estel_app.base_state import SUPABASE_API, State
from estel_app.pages.sequ_diseny import State_DisenySeq
from estel_app.pages.llista_posicions import State_LlistaPos
from estel_app.login import require_login
from estel_app.model.Sequencia_row import Sequencia_row
from estel_app.model.Llista_posicions_row import Llista_posicions_row



class State_EditarPos(State_LlistaPos):
    pass
    


# Barra navegació
def navbar():
    return rx.hstack(
        rx.button(
            rx.icon(tag="chevron-left"),
            #variant="soft",
            size="2",
            on_click=rx.redirect("/llista_pos")
        ),
        rx.button(
            rx.icon(tag="home"),
            #variant="soft",
            size="2",
            on_click=rx.redirect("/")
        ),
       rx.hstack(
            #rx.image(src="/favicon.ico", width="2em"),
            rx.text("Editar posició", font_size="1.1em", color="gray"),
        ),
        rx.spacer(),
        rx.button(
            "?",
            #variant="soft",
            size="2",
            on_click=rx.redirect("/")
        ),
        rx.button(
            rx.icon(tag="plus"),
            #variant="soft",
            size="2",
            on_click=rx.redirect("/")
        ),
        #rx.color_mode.button(rx.color_mode.icon(), float="right"),

        align="center",
        position="fixed",
        top="0px",
        background_color="#E6F4FE",
        padding="0.5em",
        height="3em",
        width="100%",
        z_index="5",
    )



@require_login
def editar_posicio() -> rx.Component:

    return rx.fragment(
        rx.vstack(
            #navbar(),
            rx.slider(min=1, max=144, step=1,
                default_value=[10,20],
                margin_top="150px"),
            rx.flex(
            rx.slider(default_value=[25], radius="none"),
            rx.slider(default_value=[25], radius="small"),
            rx.slider(default_value=[25], radius="full"),
            direction="column",
            spacing="4",
            width="100%",
            )
        )
)
