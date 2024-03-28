from .SupabaseAPI import SupabaseAPI
from estel_app.model.User_row import User_row

SUPABASE_API = SupabaseAPI()

async def hello(nom: str) -> str:
    return nom

async def users() -> list[User_row]:
    return SUPABASE_API.users()