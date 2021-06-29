import os

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

IMAGE_PATH = os.getenv('IMAGE_PATH')
