import os
from dotenv import load_dotenv


def load_environment():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    else:
        exit(-1)
