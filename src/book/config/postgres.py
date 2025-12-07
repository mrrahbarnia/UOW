from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQL(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRESQL__")

    HOST: str
    PORT: str
    DATABASE: str
    USERNAME: str
    PASSWORD: str
    DRIVER: str = "asyncpg"

    def get_url(self):
        return f"postgresql+{self.DRIVER}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
