from requests.models import PreparedRequest
from pollboy.logger import get_logger
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import json


log = get_logger(__name__)


def get_sender(settings):
    return f'{settings["from_name"]} <{settings["from_email"]}>'


def get_body(recipient, feed_item, settings):
    # this handles the query params correctly for the unsub URL
    body = feed_item.description
    body += "<p>---</p>"
    footer = ""

    if settings.get('site_name') and settings.get('site_url'):
        footer += f'&copy; {datetime.now().year} <a href="{settings["site_url"]}">{settings["site_name"]}</a>'

    if settings.get('unsubscribe_url'):
        req = PreparedRequest()
        req.prepare_url(settings['unsubscribe_url'], {'email':recipient})
        if footer != "":
            footer += " | "
        footer += f'<a href="{req.url}">Unsubscribe</a>'

    body += f'<p>{footer}</p>'

    return body


def get_html_message(recipient, feed_item, settings):
    html_message = MIMEText(get_body(recipient, feed_item, settings), 'html')
    html_message['Subject'] = f'{settings["subject_prefix"]}{feed_item.title}'
    html_message['From'] = get_sender(settings)
    html_message['To'] = recipient
    return html_message


def notify(feed_item, settings):
    recipients = []
    try:
        with open(settings['recipient_db']) as json_file:
            recipients = json.load(json_file)
            log.debug(f'Sending email notifications. Loaded {len(recipients)} recipient(s).')
    except:
        log.exception('Error occurred reading recipient db')

    with smtplib.SMTP_SSL(settings['smtp_server'], settings['smtp_port']) as server:
       server.login(settings['smtp_username'], settings['smtp_password'])
       
       for recipient in recipients:
           message = get_html_message(recipient, feed_item, settings)
           server.sendmail(get_sender(settings), recipient, message.as_string())

