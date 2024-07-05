from pathlib import Path

import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

logging.getLogger('httpx').setLevel(logging.WARNING)

TO_MB = 1024 * 1024


type AnyPath = str | Path
