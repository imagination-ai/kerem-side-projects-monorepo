import os

from common.config import CommonSettings


class StyleAppSettings(CommonSettings):

    DOCUMENT_LENGTH: int = 1000
    CROSS_VALIDATION: int = 4
    TEST_PERCENTAGE: float = 0.2
    MIN_DF: int = 1
    NUM_DOC: int = 100
    NGRAM_MIN: int = 1
    NGRAM_MAX: int = 2
    N_JOBS: int = os.cpu_count() - 1
    VECTORIZER: str = "hashing-vectorizer"  # or 'tf-idf'
    N_FEATURES = 2**20


style_app_settings = StyleAppSettings(_env_file=".env")

print(style_app_settings)
