from pydantic_settings import BaseSettings


class PostgreSQL(BaseSettings):
    HOST: str
    PORT: str
    DATABASE: str
    USERNAME: str
    PASSWORD: str
    DRIVER: str = "asyncpg"

    @property
    def get_url(self):
        return f"postgresql+{self.DRIVER}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"
