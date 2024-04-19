"""Main app module to demo local authentication."""
import reflex as rx

from .base_state import State, SUPABASE_API, SUPABASE_URL, SUPABASE_KEY
from .login import require_login
from .registration import registration_page as registration_page

from estel_app.api.api import hello, users, cua_lista
from estel_app.components.cua_data import cua_data
from fastapi import Request



class StateApp(rx.State):

    def prova(self):
        print("Que pasa")


#@rx.page(on_load=State.set_cua_info)
@rx.page()
def index() -> rx.Component:
    """Render the index page.

    Returns:
        A reflex component.
    """
    return rx.fragment(
        rx.color_mode.button(rx.color_mode.icon(), float="right"),
        rx.vstack(
            rx.heading("Welcome to my homepage!", font_size="2em"),
            rx.link("Protected Page", href="/protected"),
            rx.button("botó", on_click=State.pag_protegida),

            rx.heading(f"POST: {State.post_web_cua}", font_size="2em"),

            #rx.script("import { createClient } from '@supabase/supabase-js'"),
            #rx.script(f"const supabase = createClient({SUPABASE_URL}, {SUPABASE_KEY})"),
            #rx.script("supabase.channel('todos').on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'todos' }, handleInserts).subscribe()"),

            rx.cond(
                State.cua_info,
                rx.vstack(
                    rx.text("Destacado"),
                    rx.flex(
                        rx.foreach(
                            State.cua_info,
                             cua_data
                        ),
                        flex_direction=["column", "row"],
                        spacing="2"
                    ),
                    spacing="4",
                    #on_mount=State.set_cua_info
                )
            ),

            spacing="2",
            padding_top="10%",
            align_items="center",
        ),
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


app = rx.App(theme=rx.theme(has_background=True, accent_color="orange"))
app.add_page(index)
app.add_page(protected)

app.api.add_api_route("/hola/{nom}", hello)
app.api.add_api_route("/users", users)
app.api.add_api_route("/cua", cua_lista)

@app.api.post("/web_cua")
def nyx():
    SUPABASE_API.POST_web_cua += 1
    print("Dunqui net")
    #self.set_cua_info()
    return SUPABASE_API.POST_web_cua

"""
@app.api.post("/web_cua")
async def receive_webhook(request: Request):
    data = await request.json()
    # Process your data here
    print("Dunqui net -> 33")
    State.set_cua_info()
    #return {"message": "Webhook received!"}
"""


#app = rx.App(theme=rx.theme(has_background=True, accent_color="orange"))
#app.api.add_api_route("/web_cua", nyx)

