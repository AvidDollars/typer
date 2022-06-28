from os import path

APP_DIR = path.dirname(path.abspath(__file__))
LOG_DIR = path.abspath("logs")

CONFIG_FILE_NAME = ".env.yml"

# SENDING EMAILS
EMAIL_TEMPLATE_DIR = path.abspath("email_templates")
REGISTER_TEMPLATE_FILE_NAME = "registration.html"
