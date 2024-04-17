from .SupabaseAPI import SupabaseAPI
from estel_app.model.User_row import User_row
from estel_app.model.Cua_row import Cua_row


SUPABASE_API = SupabaseAPI()

async def hello(nom: str) -> str:
    return nom

async def users() -> list[User_row]:
    return SUPABASE_API.users()

async def cua_lista() -> list[Cua_row]:
    return SUPABASE_API.cua_list()

async def cua_web():
    print("Dunqui")
    #return SUPABASE_API.cua_list()
