from pathlib import Path

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

# Get the root logger
logger = logging.getLogger()


TO_MB = 1024 * 1024


type AnyPath = str | Path
