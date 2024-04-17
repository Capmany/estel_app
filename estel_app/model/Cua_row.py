import reflex as rx
import datetime

class Cua_row(rx.Base):
    id: int
    estat: int
    sequencia_id: int
    entrada: str
    sortida: str
