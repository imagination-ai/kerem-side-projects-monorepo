from pydantic import BaseSettings, constr

Environment = constr(regex="^(local|dev|stage|prod)$")


class Settings(BaseSettings):
    API_BASE_URL: str = "/api/v1"

    class Config:
        case_sensitive = True


settings = Settings(_env_file=".env")
print(settings)
