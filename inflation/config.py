from common.config import CommonSettings


class InflationAppSettings(CommonSettings):

    APP_PORT: int = 8000

    CRAWLER_BUCKET: str = "inflation-project-crawler-output"
    PARSER_BUCKET: str = "inflation-project-parser-output"
    MISC_BUCKET: str = "projects-misc"

    class Config:
        case_sensitive = True


inflation_app_settings = InflationAppSettings(_env_file=".env")
print(inflation_app_settings)
