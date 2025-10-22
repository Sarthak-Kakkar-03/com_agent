# settings.py
import os
from dotenv import load_dotenv

# Load .env only when running locally; in Docker/AWS, env vars are provided by the runtime.
load_dotenv(override=False)

class Settings:
    # Third-party keys
    DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")
    LANGCHAIN_TRACING_V2: str | None = os.getenv("LANGCHAIN_TRACING_V2", "true")
    LANGCHAIN_ENDPOINT: str | None = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    LANGCHAIN_API_KEY: str | None = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT: str | None = os.getenv("LANGCHAIN_PROJECT", "Communication_Assistant")

    # Mail creds (use an App Password for Gmail)
    BOT_MAIL_ID: str | None = os.getenv("BOT_MAIL_ID")
    BOT_MAIL_PASSWORD: str | None = os.getenv("BOT_MAIL_PASSWORD")

    # If you want these exported to child processes at runtime:
    def export_to_environ(self) -> None:
        os.environ["LANGCHAIN_TRACING_V2"] = self.LANGCHAIN_TRACING_V2 or "true"
        if self.LANGCHAIN_ENDPOINT: os.environ["LANGCHAIN_ENDPOINT"] = self.LANGCHAIN_ENDPOINT
        if self.LANGCHAIN_API_KEY: os.environ["LANGCHAIN_API_KEY"] = self.LANGCHAIN_API_KEY
        if self.LANGCHAIN_PROJECT: os.environ["LANGCHAIN_PROJECT"] = self.LANGCHAIN_PROJECT

settings = Settings()
