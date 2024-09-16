from os import getenv

from config.utils import str_to_bool

DEBUG = str_to_bool(val=getenv("DEBUG", default="0"))

DB_NAME = getenv("POSTGRES_DB")
DB_HOST = getenv("POSTGRES_HOST")
DB_PORT = getenv("POSTGRES_PORT")
DB_USER = getenv("POSTGRES_USER")
DB_PASSWORD = getenv("POSTGRES_PASSWORD")
