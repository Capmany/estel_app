import reflex as rx

from estel_app.base_state import SUPABASE_API, State
from estel_app.login import require_login
from estel_app.model.Sequencia_row import Sequencia_row



class State_DisenySeq(State):
    
    sequencia_row: Sequencia_row = Sequencia_row()

    @rx.var
    def seq_info(self) -> list[Sequencia_row]:
        #print(self.authenticated_user.id)
        return SUPABASE_API.sequencies(self.authenticated_user.id)
    
    def llista_sequencia(self, seq_row: Sequencia_row):
        #print(seq_row)
        self.sequencia_row= Sequencia_row(**seq_row)
        return rx.redirect("/llista_seq")



# Barra navegació
def navbar():
    return rx.hstack(
        rx.button(
            rx.icon(tag="home"),
            #variant="soft",
            size="2",
            on_click=rx.redirect("/")
        ),
        rx.hstack(
            #rx.image(src="/favicon.ico", width="2em"),
            rx.text("Seqüències", font_size="1.2em", color="gray"),
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
def sequ_disseny() -> rx.Component:

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
                State_DisenySeq.seq_info,
                # mostrar la taula de la cua actual
                rx.vstack(
                    rx.text.em("nom", margin_left="15px", color="gray"),
                    rx.foreach(
                        State_DisenySeq.seq_info, lambda fila:
                        rx.hstack(
                            rx.text(fila.nom),
                            rx.spacer(),
                            rx.flex(
                                # Editar seqüencia
                                rx.button(
                                    rx.icon(tag="pencil-line"),
                                    size="2",
                                    on_click=State_DisenySeq.llista_sequencia(fila)
                                ),
                                # Eliminar
                                rx.button(
                                    rx.icon(tag="trash-2"),
                                    size="2",
                                ),
                                # Simulació
                                rx.button(
                                    rx.icon(tag="play"),
                                    size="2",
                                ),
                                # Enviar a l'estel
                                rx.button(
                                    rx.icon(tag="sparkles"),
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
                # l'estel està lliure
                rx.flex(
                    rx.text("l'estel està lliure")
                )
            ),

            spacing="2",
            padding_top="3em",
            align_items="center",
            width="100%"
        ),
        width="100%"
    )