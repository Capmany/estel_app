import reflex as rx

class User_row(rx.Base):
    id: int
    username: str
    password_hash: str
    enabled: bool
