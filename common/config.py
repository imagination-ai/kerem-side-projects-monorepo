from pydantic import BaseSettings, validator


class CommonSettings(BaseSettings):
    API_BASE_URL: str = "/api/v1"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080

    MISC_BUCKET: str = "projects-misc"

    ENVIRONMENT: str = "local"

    @validator("ENVIRONMENT", pre=True)
    def validate_env(cls, v):
        if v in {"local", "docker", "dev", "stage", "prod", "test"}:
            return v

    class Config:
        case_sensitive = True


settings = CommonSettings(_env_file=".env")
print(settings)
