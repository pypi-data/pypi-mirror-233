from pathlib import Path
import logging

APP_DIR = Path('~/.config/pollboy').expanduser()

DB_FILE = Path(APP_DIR / 'db.json')
CONFIG_FILE = Path(APP_DIR / 'config.yaml')
LOG_FILE = Path(APP_DIR / 'pollboy.log')

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

FILE_LOG_MAX_BYTES = 1024 * 1024 * 5 #5MB
FILE_LOG_BACKUP_COUNT = 4
