import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

CHANNEL_ID = os.environ.get("CHANNEL_ID")
WRITE_KEY = os.environ.get("WRITE_KEY")
CAMERA_NUMBER = os.environ.get("CAMERA_NUMBER")
