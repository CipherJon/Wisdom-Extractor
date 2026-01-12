import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    # Model Parameters
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 150))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

    # API Endpoints
    OPENAI_API_URL = os.getenv(
        "OPENAI_API_URL", "https://api.openai.com/v1/chat/completions"
    )
    YOUTUBE_API_URL = os.getenv(
        "YOUTUBE_API_URL", "https://www.googleapis.com/youtube/v3"
    )

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "app.log")

    # Database Configuration
    DB_NAME = os.getenv("DB_NAME", "wisdom_extractor.db")
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")

    # YouTube Video Download Configuration
    VIDEO_DOWNLOAD_DIR = os.getenv("VIDEO_DOWNLOAD_DIR", "downloads/videos")
    TRANSCRIPT_DOWNLOAD_DIR = os.getenv(
        "TRANSCRIPT_DOWNLOAD_DIR", "downloads/transcripts"
    )

    # AI Processing Configuration
    INSIGHT_CATEGORIES = os.getenv(
        "INSIGHT_CATEGORIES", "key_insights,actionable_tips,quotes"
    ).split(",")
    MAX_INSIGHT_LENGTH = int(os.getenv("MAX_INSIGHT_LENGTH", 500))


# Initialize configuration
config = Config()
