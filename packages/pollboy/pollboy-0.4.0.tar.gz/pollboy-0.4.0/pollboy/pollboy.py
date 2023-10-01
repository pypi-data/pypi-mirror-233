from pollboy.config import Config
from pollboy.db import DB
from pollboy.logger import get_logger
from pollboy import settings
from time import mktime
import feedparser
from pathlib import Path

config = Config()
db = DB()
log = get_logger(__name__)


def get_parsed_feed(feed_url):
    return feedparser.parse(feed_url)


def get_latest_post(feed_url):
    parsed_feed = get_parsed_feed(feed_url)

    if(len(parsed_feed.entries) == 0):
        return False

    return parsed_feed.entries[0]


def get_post_timestamp(feed_item):
    return mktime(feed_item.published_parsed)


def load_notifier_modules():
    notifiers = {}
    for py_file in Path(Path(__file__).parent / 'notifiers').glob('*.py'):
        mod_name = py_file.stem
        notifiers[mod_name] = __import__(f'pollboy.notifiers.{mod_name}', fromlist=[''])
    return notifiers


def notifier_module_valid(name, module):
    if module == None:
        log.error(f'"{name}" notifier does not exist')
        return False

    if not hasattr(module, 'notify'):
        log.error(f'"{name} notifier module does not contain a notify() function')
        return False
    
    return True


def send_notifications_for_post(notifiers, feed_url, feed_item):
    notifier_modules = load_notifier_modules()
    notification_history = db.get(feed_url, {})
    post_timestamp = get_post_timestamp(feed_item)

    for notifier in notifiers:
        module = notifier_modules.get(notifier)
        last_notification = notification_history.get(notifier)
        notifier_settings = notifiers[notifier]

        if not notifier_module_valid(notifier, module):
            continue

        if last_notification == None or last_notification < post_timestamp:
            try:
                module.notify(feed_item, notifier_settings)
                notification_history[notifier] = post_timestamp
                if not config.get('disable_db', False):
                    db.set(feed_url, notification_history)
            except Exception:
                log.exception(f'Error occurred sending "{notifier}" notification')
        else:
            log.debug(f'Already sent {notifier} notification for post: {feed_item.title}')
    

def run():
    """
    Loop through all configured RSS feeds, pull the latest post, and send notifications to configured channels if needed
    """
    if not config.config_file_exists():
        config.initialize()
        log.info(f'Config file created at {settings.CONFIG_FILE}. Update this file and run again.')
    else:
        config.initialize()
        for feed in config.get('feeds'):
            latest = get_latest_post(feed['rss_url'])
            if latest != False:
                send_notifications_for_post(feed['notify'], feed['rss_url'], latest)
            else:
                log.info('Feed does not contain any posts')
            

if __name__ == '__main__':
    run()
