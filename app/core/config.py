from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    ENV: str
    DEBUG: bool
    DATABASE_URL: str
    LLM_PROVIDER: str
    GEMINI_API_KEY: str
    GEMINI_MODEL: str
    LLM_TEMPERATURE: float
    LLM_TIMEOUT_SECONDS: int
    INTERNAL_LLM_URL: str | None = None
    INTERNAL_LLM_TIMEOUT: int = 60
    MAX_COMMENT_WORDS: int
    MAX_COMMENT_SENTENCES: int
    ALLOW_EXTERNAL_FACTS: bool
    ALLOW_STATISTICS: bool
    REQUIRE_HUMAN_APPROVAL: bool
    ALLOW_EDIT_AFTER_APPROVAL: bool
    AUTO_POSTING_ENABLED: bool
    MAX_POSTS_PER_DAY: int
    MAX_POSTS_PER_TARGET: int
    POSTING_RETRY_LIMIT: int
    POSTING_RETRY_BACKOFF_SECONDS: int
    LOG_LEVEL: str
    ENABLE_AUDIT_LOGS: bool

    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()
