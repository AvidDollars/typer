from os import path

# DIRECTORIES
APP_DIR = path.dirname(path.abspath(__file__))
LOG_DIR = path.abspath("logs")
EMAIL_TEMPLATE_DIR = path.abspath("email_templates")

# CONFIG
CONFIG_FILE_NAME = ".env.yml"

# WILL CATCH MOST OF THE INVALID EMAILS
EMAIL_VALIDATOR_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# EMAIL TEMPLATES
REGISTER_TEMPLATE_FILE_NAME = "registration.html"

# DB ERROR CODES
UNIQUE_CONSTRAINT_VIOLATED = "23505"
