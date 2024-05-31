import hashlib
from modules import logger

logger = logger.setup_logger(__name__)


def file_md5(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            return hashlib.md5(file.read()).hexdigest()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error hashing file: {file_path}")
        logger.error(e)
        return None
