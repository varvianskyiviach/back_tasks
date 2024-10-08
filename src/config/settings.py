from os import getenv
from pathlib import Path

from config.utils import str_to_bool

SRC_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SRC_DIR.parent

DEBUG = str_to_bool(val=getenv("DEBUG", default="0"))

ENVIRONMENT = getenv("ENVIRONMENT")

DB_NAME = getenv("POSTGRES_DB")
DB_HOST = getenv("POSTGRES_HOST")
DB_PORT = getenv("POSTGRES_PORT")
DB_USER = getenv("POSTGRES_USER")
DB_PASSWORD = getenv("POSTGRES_PASSWORD")

FIRST_SUPERUSER_EMAIL = getenv("SUPERUSER_EMAIL")
FIRST_SUPERUSER_PASSWORD = getenv("SUPERUSER_PASSWORD")
FIRST_SUPERUSER_FIRST_NAME = getenv("SUPERUSER_FIRST_NAME")
FIRST_SUPERUSER_LAST_NAME = getenv("SUPERUSER_LAST_NAME")

ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

SECRET_KEY: str = getenv("SECRET_KEY")
