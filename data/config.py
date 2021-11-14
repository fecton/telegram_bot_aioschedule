from os import getenv
from dotenv import load_dotenv

from .long_messages import content

load_dotenv()  # Initialization

DB_NAME = "days_textes.sqlite3"  # Database name

TOKEN = getenv("TOKEN")  # Get token
SUPER_USERS = [int(getenv("OWNER"))]  # here is you (mean admin)
