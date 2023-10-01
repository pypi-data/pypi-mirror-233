from pollboy.logger import get_logger
from mailersend import emails
import json

log = get_logger(__name__)

def get_email_objects(recipients, feed_item, settings):
    objs = []

    for email in recipients:
        objs.append({
            "from": {
                "email": settings["from_email"],
                "name": settings["from_name"]
            },
            "to": [
                {
                    "email": email,
                }
            ],
            "subject": settings.get("subject_prefix", '') + feed_item.title,
            "html": feed_item.description,
            "template_id": settings.get("template_id")
        })

    return objs
      
def notify(feed_item, settings):
    try:
        with open(settings['recipient_db']) as json_file:
            recipients = json.load(json_file)
            mail_list = get_email_objects(recipients, feed_item, settings)
            mailer = emails.NewEmail(settings['api_key'])
            log.debug(f'Sending email to {len(mail_list)} recipient(s).')
            mailer.send_bulk(mail_list)
    except:
        log.exception('Error occurred reading recipient db')
