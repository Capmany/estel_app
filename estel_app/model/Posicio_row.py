import reflex as rx

class Posicio_row(rx.Base):
    id: int = -1
    llista_id: int = -1
    inici_tram: int = 0
    final_tram: int = 0
    flag_repetir: bool = False
    espai: int = 0
    puntes: int = 63
    flag_estel_gran: bool = True
    color: str = "#00FF00"
