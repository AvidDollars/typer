import os.path
from os import path

# DIRECTORIES
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
APP_DIR = path.dirname(path.abspath(__file__))
LOG_DIR = path.abspath("logs")
EMAIL_TEMPLATE_DIR = path.join(BACKEND_DIR, "email_templates")
TEST_DB_SEED_DIR = path.join(APP_DIR, "tests/test_db_seed")

# CONFIG
CONFIG_FILE_NAME = ".env.yml"

# WILL CATCH MOST OF THE INVALID EMAILS
EMAIL_VALIDATOR_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# EMAIL TEMPLATES
REGISTER_TEMPLATE_FILE_NAME = "registration.html"

# DB ERROR CODES
INVALID_FOREIGN_KEY = "23503"
UNIQUE_CONSTRAINT_VIOLATED = "23505"

# OTHER
USER_TEXTS_MAX_COUNT = 10
