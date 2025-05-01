import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date

load_dotenv(override=True)

class Logger:
    def __init__(self, debugconf:str):
        self.Debug = debugconf
    
    def get_logger(self, name: str = "default") -> logging.Logger:
        log_dir = Path.cwd() / ".logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{date.today()}_app.log"

        logger = logging.getLogger(name)

        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            debug_flag = self.Debug.lower() == "true"
            console_level = logging.DEBUG if debug_flag else logging.INFO

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(console_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

# global default logger: -> useage everywhere
app_logger = Logger(os.getenv("DEBUG", "False")).get_logger("app")
