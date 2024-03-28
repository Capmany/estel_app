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
    