"""Main app module to demo local authentication."""
import reflex as rx
from estel_app.pages.sequ_diseny import sequ_disseny
from estel_app.pages.llista_sequencia import llista_sequencia
from estel_app.pages.llista_posicions import llista_posicions
from estel_app.pages.editar_posicio import editar_posicio

from estel_app.utils_dibuix.llums_encesos import llumsEncesos

from .base_state import State, SUPABASE_API, SUPABASE_URL, SUPABASE_KEY
from .login import require_login
from .registration import registration_page as registration_page

from estel_app.api.api import hello, users, cua_lista
from estel_app.components.cua_data import cua_data
from fastapi import Request





@rx.page(on_load=State.set_cua_info)
#@rx.page()
def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    return rx.fragment(
        rx.color_mode.button(rx.color_mode.icon(), float="right"),
        rx.vstack(

            rx.link(f"Logout {State.authenticated_user.username}", href="/", on_click=State.do_logout),
            rx.heading("Welcome to my homepage!", font_size="2em", align="center"),
            rx.link("Protected Page", href="/protected"),

            rx.card(
                rx.flex(
                    rx.image(src="/puntaAG.png", width="100px", heht="auto"),
                    rx.vstack(
                        rx.text("Estel de Capmany", size="8"),
                        rx.spacer(),
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                rx.icon(tag="notebook-text"),
                                "info",
                                variant="soft",
                                size="3"
                            ),
                            width="100%",
                        ),
                    ),
                    spacing="4"
                )
            ),
            rx.flex(
                rx.button("Seqüències preestablertes", on_click=rx.redirect("/llumsEncesos"), width= "250px",variant="surface",size="3"),
                rx.button("Disenyar seqüències", on_click=rx.redirect("/disseny_seq"), width= "250px",variant="surface",size="3"),
                spacing= "4",
                flex_wrap="wrap",
                align="center",
                justify="center"
            ),

            #rx.heading(f"POST: {State.post_web_cua}", font_size="2em"),


            rx.heading(f"Estat de la cua per entrar a l'estel", font_size="1.5em", padding_top="2%"),
            rx.cond(
                State.cua_info,
                # mostrar la taula de la cua actual
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("usuari", justify="center"),
                            rx.table.column_header_cell("seqüència", justify="center"),
                            rx.table.column_header_cell("previsió", justify="center"),
                            rx.table.column_header_cell("XXX", justify="center"),
                        ),
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.cua_info, lambda fila: 
                                rx.table.row(
                                    rx.table.row_header_cell(fila[0], justify="center"),
                                    rx.table.cell(fila[1], justify="center"),
                                    rx.table.cell(fila[2], justify="center"),
                                    rx.table.cell(
                                        rx.button(
                                            rx.icon(tag="trash-2"),
                                            #color_scheme="red",
                                            size="2",
                                            
                                        ),
                                        justify="center",
                                    ),
                                    align="center",
                                    background_color="#C4E8D1",
                                )

                        ),
                    ),
                    size="3",
                    width="100%",
                    padding_left="5px",
                    padding_right="5px",
                ),
                # l'estel està lliure
                rx.flex(
                    rx.text("l'estel està lliure")
                )
            ),

            spacing="2",
            padding_top="10%",
            align_items="center",
            width="100%"
        ),
        width="100%"
    )


@require_login
def protected() -> rx.Component:
    """Render a protected page.

    The `require_login` decorator will redirect to the login page if the user is
    not authenticated.

    Returns:
        A reflex component.
    """
    return rx.vstack(
        rx.heading(
            "Protected Page for ", State.authenticated_user.username, font_size="2em"
        ),
        rx.link("Home", href="/"),
        rx.link("Logout", href="/", on_click=State.do_logout),
    )


app = rx.App(theme=rx.theme(has_background=True, accent_color="blue"))
app.add_page(index)
app.add_page(protected)
app.add_page(sequ_disseny, route="/disseny_seq", title="Dissenyar seqüències")
app.add_page(llista_sequencia, route="/llista_seq", title="Llista d'una seqüència")
app.add_page(llista_posicions, route="/llista_pos", title="Posició d'una seqüència")
app.add_page(editar_posicio, route="/editar_pos", title="Editar posició d'una seqüència")

app.add_page(llumsEncesos, route="/llumsEncesos")

app.api.add_api_route("/hola/{nom}", hello)
app.api.add_api_route("/users", users)
app.api.add_api_route("/cua", cua_lista)


@app.api.post("/web_cua")
def nyx():
    SUPABASE_API.POST_web_cua += 1
    SUPABASE_API.POST_rebut = True
    print("Dunqui net")
    SUPABASE_API.estat.pag_protegida()
    #self.set_cua_info()
    return SUPABASE_API.POST_web_cua


#app = rx.App(theme=rx.theme(has_background=True, accent_color="orange"))
#app.api.add_api_route("/web_cua", nyx)

