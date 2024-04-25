from passlib.context import CryptContext

import reflex as rx

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User_row(rx.Base):
    id: int
    username: str
    password_hash: str
    enabled: bool

    @staticmethod
    def hash_password(secret: str) -> str:
        """Hash the secret using bcrypt.

        Args:
            secret: The password to hash.

        Returns:
            The hashed password.
        """
        return pwd_context.hash(secret)

    def verify(self, secret: str) -> bool:
        """Validate the user's password.

        Args:
            secret: The password to check.

        Returns:
            True if the hashed secret matches this user's password_hash.
        """
        #return secret == self.password_hash
        return pwd_context.verify(
            secret,
            self.password_hash,
        )