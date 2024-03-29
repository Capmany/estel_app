import reflex as rx
import datetime

class Authsession_row(rx.Base):
    id: int
    user_id: int
    session_id: str
    expiration: datetime.datetime

