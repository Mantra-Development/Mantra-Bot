from pydantic import BaseSettings


class PostgresConfig(BaseSettings):
    user: str
    db: str
    password: str
    port: str
    host: str

    class Config:
        env_file = ".env"
        env_prefix = "postgres_"


db_config = PostgresConfig()
