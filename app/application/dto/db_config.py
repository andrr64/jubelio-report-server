# app/domain/entities.py
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DBConfig:
    host: str
    port: int
    username: str
    password: str  # Nanti pake SecretStr kalau mau lebih aman
    database: str
    schema: Optional[str] = "public"

    @property
    def dsn(self) -> str:
        """
        Returns the standard PostgreSQL Data Source Name (DSN) string.
        """
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def __hash__(self):
        return hash(self.dsn)
