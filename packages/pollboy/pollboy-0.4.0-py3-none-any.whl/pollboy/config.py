from pollboy import settings

# system imports
from pathlib import Path

# 3rd party imports
import yaml


class Config():
    """Wrapper around config file to get/set values and update the config file"""

    DEFAULTS = {
        'feeds': [
            {
                'rss_url': 'https://example.com/index.xml',
                'notify': {
                    'telegram': {
                        'token': 'your-token-here',
                        'chat_id': '@yourChannelUsername'
                    }
                }
            }
        ]
    }

    REQUIRED_KEYS = ['feeds']

    _config = None

    def __init__(self, config=None, file_path=None):
        """Initialize the config

        Keyword arguments:
        config -- Optional dict to initialize config
        file_path -- Optional path to override the default file location
        """

        self._config_path = file_path or settings.CONFIG_FILE

        if config is not None:
            self._config = config
        

    def initialize(self):
        if self._config is not None:
            return 
        elif self.config_file_exists():
            self.load()
        else:
            self.reset_to_defaults()


    def get(self, key, default=None):
        """Get the value from the config for the given key"""
        return self._config.get(key, default)

    def set(self, key, value):
        """Set the value in the config for the given key. The file will be immediately saved"""
        self._config[key] = value
        self.save()

    def save(self):
        """Write the config to disk"""
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(yaml.dump(self._config), encoding='utf-8')

    def is_valid(self):
        """Whether or not the config file is valid"""
        for key in self.REQUIRED_KEYS:
            if key not in self._config or not self._config[key]:
                return False
        return True

    def load(self):
        """Load the config yaml from disk into the config class level dict variable"""
        if self.config_file_exists():
            with self._config_path.open(encoding='utf-8') as file:
                self._config = yaml.load(file, Loader=yaml.FullLoader)

    def config_file_exists(self):
        """Whether or not the config file exists on disk"""
        return self._config_path.exists()

    def reset_to_defaults(self):
        """Restore the config file to the original defaults defined in DEFAULTS"""
        self._config = self.DEFAULTS
        self.save()

