from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_DSB: str
    SCHEMA: str = "public"
