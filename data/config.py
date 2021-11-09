from os import getenv
from dotenv import load_dotenv
from .long_messages import content

load_dotenv()  # Initialization

DB_NAME = "list"  # Database name

TOKEN = getenv("TOKEN")  # Get token
SUPER_USERS = [int(getenv("OWNER"))]

