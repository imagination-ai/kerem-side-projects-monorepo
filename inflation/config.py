from pydantic import BaseSettings, constr

Environment = constr(regex="^(local|dev|stage|prod)$")


class Settings(BaseSettings):
    API_BASE_URL: str = "/api/v1"
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"

    class Config:
        case_sensitive = True


settings = Settings(_env_file=".env")
print(settings)
