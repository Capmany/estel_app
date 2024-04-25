import os
import dotenv
import datetime
from supabase import create_client, Client
from estel_app.model.User_row import User_row
from estel_app.model.Cua_row import Cua_row
from estel_app.model.Sequencia_row import Sequencia_row
from estel_app.model.Llista_posicions_row import Llista_posicions_row
from estel_app.model.Posicio_row import Posicio_row


class SupabaseAPI:

    POST_web_cua = 0
    POST_rebut = False

    dotenv.load_dotenv()

    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


    def __init__(self) -> None:
        if self.SUPABASE_URL != None and self.SUPABASE_KEY != None:
            self.supabase: Client = create_client(
                self.SUPABASE_URL, self.SUPABASE_KEY)



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
    
    # Retorna la cua
    # Es una llista de llistes, cada sub-llista és un registre:
    # ["usuari" , "nom seqüència", "previsió per entrar a l'estel ó en l'estel", True ó False si el client pot treure la seqüencia de la cua]
    def cua_list(self) -> list[list[str,str,str,bool]]:

        response = self.supabase.table(
            "cua").select("*").order("entrada", desc=True).execute()
        cua_l = []
        if len(response.data) > 0:
            for cua_item in response.data:
                #print(cua_item)
                """
                cua_l.append(
                    Cua_row(
                        id=cua_item["id"],
                        estat=cua_item["estat"],
                        sequencia_id=cua_item["sequencia_id"],
                        entrada=cua_item["entrada"],
                        sortida= cua_item["sortida"] if cua_item["sortida"] != None else ""
                    )
                )
                """
                reg = ["nom", "la estrella va canviant de colors", "en l'estel", True]
                cua_l.append(reg)
        return cua_l

    # Retorna una llista amb les seqüències d'un user
    def sequencies(self, user_id: int) -> list[Sequencia_row]:
        response = self.supabase.table("sequencia").select("*").order("nom", desc=False).eq("user_id", user_id).execute()
        seq_data = []
        if len(response.data) > 0:
            for seq_item in response.data:
                seq_data.append(
                    Sequencia_row(
                        id=seq_item["id"],
                        user_id=seq_item["user_id"],
                        nom=seq_item["nom"],
                    )
                )
        return seq_data

    # Retorna una llista de posicions d'una seqüència
    def llista_sequencia(self, sequencia_id: int) -> list[Llista_posicions_row]:
        response = self.supabase.table("llista_posicions").select("*").order("ordre", desc=False).eq("sequencia_id", sequencia_id).execute()
        seq_data = []
        if len(response.data) > 0:
            for seq_item in response.data:
                seq_data.append(
                    Llista_posicions_row(
                        id=seq_item["id"],
                        sequencia_id=seq_item["sequencia_id"],
                        durada=seq_item["durada"],
                        ordre=seq_item["ordre"]
                    )
                )
        return seq_data

    # Retorna una llista de posicions d'una Llista de posicions
    def llista_posicions(self, llista_id: int) -> list[Posicio_row]:
        response = self.supabase.table("posicio").select("*").eq("llista_id", llista_id).execute()
        seq_data = []
        if len(response.data) > 0:
            for seq_item in response.data:
                seq_data.append(
                    Llista_posicions_row(
                        id=seq_item["id"],
                        llista_id=seq_item["llista_id"],
                        inici_tram=seq_item["inici_tram"],
                        final_tram=seq_item["final_tram"],
                        flag_repetir=seq_item["flag_repetir"],
                        espai=seq_item["espai"],
                        puntes=seq_item["puntes"],
                        flag_estel_gran=seq_item["flag_estel_gran"],
                        color=seq_item["color"]
                    )
                )
        return seq_data
