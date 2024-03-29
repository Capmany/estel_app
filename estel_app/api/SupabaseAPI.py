import os
import dotenv
from supabase import create_client, Client
from estel_app.model.User_row import User_row


class SupabaseAPI:

    dotenv.load_dotenv()

    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    def __init__(self) -> None:
        if self.SUPABASE_URL != None and self.SUPABASE_KEY != None:
            self.supabase: Client = create_client(
                self.SUPABASE_URL, self.SUPABASE_KEY
            )

    # Retorna un diccionari amb tots els usuaris
    def users(self) -> list[User_row]:

        response = self.supabase.table(
            "user").select("*").order("username", desc=True).execute()
        user_data = []
        if len(response.data) > 0:
            for user_item in response.data:
                user_data.append(
                    User_row(
                        id=user_item["id"],
                        username=user_item["username"],
                        password_hash=user_item["password_hash"],
                        enabled=user_item["enabled"]
                    )
                )
        return user_data
    # Comproba si un username existeix. SI existeix, retorna les seves dades
    def exist_username(self, username: str) -> User_row:
        response = self.supabase.table("user").select("*").eq("username", username).execute()
        if len(response.data) > 0:
            user_item = response.data[0]
            return User_row(id=user_item["id"], username=user_item["username"], password_hash=user_item["password_hash"], enabled=user_item["enabled"])
        return None
    # Comproba si un user_id existeix. SI existeix, retorna les seves dades
    def exist_user_id(self, user_id: str) -> User_row:
        response = self.supabase.table("user").select("*").eq("id", user_id).execute()
        if len(response.data) > 0:
            user_item = response.data[0]
            return User_row(id=user_item["id"], username=user_item["username"], password_hash=user_item["password_hash"], enabled=user_item["enabled"])
        return None
    # Donar d'alta un nou usuari. Retorna el registre insertat
    def new_user(self, user: User_row) -> dict:
        response = self.supabase.table('user').insert({"username": user.username, "password_hash": user.password_hash, "enabled": user.enabled}).execute()
        return response.data
    

