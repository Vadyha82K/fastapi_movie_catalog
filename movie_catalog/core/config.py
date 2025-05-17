import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


API_TOKENS = frozenset(
    {
        "Q6A0JpXQWAgJQAwW__rTKA",
        "qbVvtDs3TG3W5zGJwc3YeQ",
    }
)

USERS_DB = {
    "bob": "qwerty",
    "sam": "password",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6372
REDIS_DB = 0
