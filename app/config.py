import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

MODEL = "deepseek/deepseek-chat"

MAX_ARTICLES = 20
MAX_DEALS = 10
LLM_RETRY_COUNT = 2
REQUEST_TIMEOUT = 60