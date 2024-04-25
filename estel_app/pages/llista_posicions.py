import reflex as rx

from estel_app.base_state import SUPABASE_API, State
from estel_app.pages.sequ_diseny import State_DisenySeq
from estel_app.pages.llista_sequencia import State_LlistaSeq
from estel_app.login import require_login
from estel_app.model.Sequencia_row import Sequencia_row
from estel_app.model.Llista_posicions_row import Llista_posicions_row
from estel_app.model.Posicio_row import Posicio_row



class State_LlistaPos(State_LlistaSeq):
    
    posicio_row: Posicio_row = Posicio_row()

    @rx.var
    def llista_pos_info(self) -> list[Posicio_row]:
        #print(self.authenticated_user.id)
        return SUPABASE_API.llista_posicions(self.llista_posicions_row.id)

    def editar_pos(self, pos_row: Posicio_row):
        #print(llista_pos_row)
        self.posicio_row= Posicio_row(**pos_row)
        return rx.redirect("/editar_pos")



# Barra navegació
def navbar():
    return rx.hstack(
        rx.button(
            rx.icon(tag="chevron-left"),
            #variant="soft",
            size="2",
            on_click=rx.redirect("/llista_seq")
        ),
        rx.button(
            rx.icon(tag="home"),
            #variant="soft",
            size="2",
            on_click=rx.redirect("/")
        ),
       rx.hstack(
            #rx.image(src="/favicon.ico", width="2em"),
            rx.text("Posició seqüència", font_size="1.1em", color="gray"),
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
def llista_posicions() -> rx.Component:

    return rx.fragment(
        navbar(),
        rx.vstack(
            rx.hstack(
                rx.spacer(),
                rx.link(rx.text(rx.text.em("logout"), rx.text.strong(f"  {State.authenticated_user.username}")), href="/", on_click=State.do_logout, color="green"),
                padding_right="15px",
                padding_top="20px",
                width="100%"
            ),
            rx.cond(
                State_LlistaPos.llista_pos_info,
                rx.vstack(
                    # mostrar nom i durada de la seqüència
                    rx.hstack(
                        rx.text(rx.text.em("nom"), rx.text.strong(f"  {State_LlistaSeq.sequencia_row.nom}")), #, on_click=State.do_logout, color="gray"),
                        rx.spacer(),
                        rx.button(rx.icon(tag="pencil-line"),size="2",),
                        align="center",
                        padding_left="20px",
                        padding_right="15px",
                        padding_top="10px",
                        width="100%"
                    ),
                    # mostrar la taula de la seqüència actual
                    rx.vstack(
                        rx.text.em("durada", margin_left="15px", color="gray"),
                        rx.foreach(
                            State_LlistaPos.llista_pos_info, lambda fila:
                            rx.hstack(
                                rx.text(fila.inici_tram),
                                rx.spacer(),
                                rx.flex(
                                    # Imatge de la posició
                                    rx.image(),
                                    # Editar posició
                                    rx.button(
                                        rx.icon(tag="pencil-line"),
                                        size="2",
                                        on_click=State_LlistaPos.editar_pos(fila)
                                    ),
                                    # Eliminar
                                    rx.button(
                                        rx.icon(tag="trash-2"),
                                        size="2",
                                        disabled=True
                                    ),
                                    # Pujar
                                    rx.button(
                                        rx.icon(tag="move-up"),
                                        size="2",
                                    ),
                                    # Baixar
                                    rx.button(
                                        rx.icon(tag="move-down"),
                                        size="2",
                                    ),
                                    spacing="2",
                                    #flex_wrap="wrap",
                                ),
                                align="center",
                                width="96%",
                                padding_left="10px",
                                padding_right="10px",
                                padding_top="8px",
                                padding_bottom="8px",
                                margin_right="2%",
                                margin_left="2%",
                                background_color="#F2FAFB", #"#F2FAFB", #"#C4E8D1",
                                border_color="green", #"#107D98",
                                border_radius="10px"
                            ),
                        ),
                        width="100%",
                    ),


                    width="100%",
                ),
                # l'estel està lliure
                rx.flex(
                    rx.text("afegeix una linea a la posició")
                )
            ),

            spacing="2",
            padding_top="3em",
            align_items="center",
            width="100%"
        ),
        width="100%"
    )