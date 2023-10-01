from pollboy import settings
# system imports
from pathlib import Path
import json


class DB():

    _db = {}
    _db_path = ''

    def __init__(self, db=None, file_path=None):
        
        self._db_path = file_path or settings.DB_FILE

        if db is not None:
            self._db = db
        elif self.db_file_exists():
            self.load()
        else:
            self.reset_to_defaults()

    def get(self, key, default=None):
        return self._db.get(key, default)

    def set(self, key, value):
        self._db[key] = value
        self.save()

    def save(self):
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db_path.write_text(json.dumps(self._db), encoding='utf-8')
    
    def load(self):
        if self.db_file_exists():
            with self._db_path.open(encoding='utf-8') as file:
                self._db = json.load(file)

    def db_file_exists(self):
        return self._db_path.exists()

    def reset_to_defaults(self):
        self._db = {}
        self.save()

