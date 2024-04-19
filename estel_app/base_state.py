"""
Top-level State for the App.

Authentication data is stored in the base State class so that all substates can
access it for verifying access to event handlers and computed vars.
"""
import datetime
import os
import asyncio

import reflex as rx
from estel_app.api.api import SUPABASE_API, cua_lista
from estel_app.model.User_row import User_row
from estel_app.model.Cua_row import Cua_row
#from estel_app.model.Authsession_row import Authsession_row

from realtime.connection import Socket
from supabase import create_client, Client


AUTH_TOKEN_LOCAL_STORAGE_KEY = "_auth_token"
DEFAULT_AUTH_SESSION_EXPIRATION_DELTA = datetime.timedelta(days=7)


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

"""
#def __init__(self) -> None:
#async def inici():
print("33")
URL = f"wss://{SUPABASE_URL}.supabase.co/realtime/v1/websocket?apikey={SUPABASE_KEY}&vsn=1.0.0"
s = Socket(URL)
s.connect()
channel_1 = s.set_channel("realtime:*")
channel_1.join().on("UPDATE", State.set_cua_info)
s.listen()
    #State.set_cua_info()

#inici()
"""





class State(rx.State):
    # The auth_token is stored in local storage to persist across tab and browser sessions.
    auth_token: str = rx.LocalStorage(name=AUTH_TOKEN_LOCAL_STORAGE_KEY)

    cua_info: list[Cua_row]

    bucle = False
    
    @rx.var
    def post_web_cua(self):
        return SUPABASE_API.POST_web_cua
    
    @rx.cached_var
    def authenticated_user(self) -> User_row:
        """The currently authenticated user, or a dummy user if not authenticated.

        Returns:
            A User instance with id=-1 if not authenticated, or the User instance
            corresponding to the currently authenticated user.
        """
        response = SUPABASE_API.supabase.table("authsession").select("*").eq("session_id", self.auth_token).gte("expiration", datetime.datetime.now(datetime.timezone.utc)).limit(1).execute()
        #print(response.data)

        if len(response.data) > 0:
            return SUPABASE_API.exist_user_id(response.data[0]["user_id"])
        return User_row(id=-1, username="", password_hash="", enabled=False)
    


    @rx.cached_var
    def is_authenticated(self) -> bool:
        """Whether the current user is authenticated.

        Returns:
            True if the authenticated user has a positive user ID, False otherwise.
        """
        return self.authenticated_user.id >= 0

    async def do_logout(self) -> None:
        """Destroy AuthSessions associated with the auth_token."""
        response = SUPABASE_API.supabase.table("authsession").delete().eq("session_id", self.auth_token).execute()
        self.auth_token = self.auth_token

    async def _login(
        self,
        user_id: int,
        expiration_delta: datetime.timedelta = DEFAULT_AUTH_SESSION_EXPIRATION_DELTA,
    ) -> None:
        """Create an AuthSession for the given user_id.

        If the auth_token is already associated with an AuthSession, it will be
        logged out first.

        Args:
            user_id: The user ID to associate with the AuthSession.
            expiration_delta: The amount of time before the AuthSession expires.
        """
        if self.is_authenticated:
            self.do_logout()
        if user_id < 0:
            return
        self.auth_token = self.auth_token or self.router.session.client_token

        iso_time = (datetime.datetime.now(datetime.timezone.utc)+expiration_delta).strftime("%Y-%m-%dT%H:%M:%SZ") 
        #print(datetime.datetime.fromisoformat(iso_time))
        response = SUPABASE_API.supabase.table('authsession').insert({"user_id": user_id, "session_id": self.auth_token, "expiration": iso_time}).execute()

    @rx.background
    async def set_cua_info(self):
        async with self:
            if self.bucle: return
            self.bucle = True
            for i in range(500):
                async with self:
                    await asyncio.sleep(0.5)
                    self.cua_info = SUPABASE_API.cua_list()
                    print(f"Xavier -> {i}")
                    if self.bucle == False: break
                    yield
                #print(self.cua_info)
            async with self:
                self.bucle = False

    def pag_protegida(self):
        self.bucle = False



