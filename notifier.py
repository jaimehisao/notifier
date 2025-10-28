import os
import apprise
import logging
import logging_loki
import yaml
import click
from dotenv import load_dotenv

load_dotenv()

# Configure Loki logger
loki_url = os.getenv("LOKI_URL", "")
logger = logging.getLogger("notifier")

if loki_url:
    handler = logging_loki.LokiHandler(
        url=loki_url,
        tags={"application": "notifier"},
        version="1",
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def load_config(config_path='config.yml'):
    """Loads the notification configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

    logger = logging.getLogger("notifier")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def send_notification(title, body, urls):
    """
    Sends a notification to the specified Apprise URLs.
    """
    # TODO: Implement a reply handler for interactive notifications
    apobj = apprise.Apprise()

    for url in urls:
        if url:
            apobj.add(url)

    if not apobj.notify(body=body, title=title):
        print("Failed to send notification")
        if loki_url:
            logger.error(
                f"Failed to send notification to {urls}",
                extra={"tags": {"status": "failure"}},
            )
        return False

    print("Notification sent successfully")
    if loki_url:
        logger.info(
            f"Notification sent to {urls}",
            extra={"tags": {"status": "success"}},
        )
    return True

@click.group()
def cli():
    """A command-line tool for sending notifications."""
    pass

@cli.command()
@click.option('--title', required=True, help='The title of the notification.')
@click.option('--body', required=True, help='The body of the notification.')
@click.option('--channel', required=True, help='The notification channel to use (e.g., info, warnings).')
@click.option('--config', default='config.yml', help='Path to the configuration file.')
def send(title, body, channel, config):
    """Sends a notification to a specified channel."""
    config_data = load_config(config)
    if not config_data:
        return

    channels = config_data.get('channels', {})
    if channel not in channels:
        print(f"Error: Channel '{channel}' not found in the configuration file.")
        return

    urls = channels[channel]
    send_notification(title, body, urls)

if __name__ == '__main__':
    cli()
if __name__ == '__main__':
    # Example usage:
    # Set the APPRISE_URLS environment variable to a comma-separated list of Apprise URLs.
    # For example: "mailto://user:pass@gmail.com,tgram://bottoken/chatid"
    # Set the LOKI_URL environment variable to your Loki instance's push API endpoint.
    # For example: "http://localhost:3100/loki/api/v1/push"
    apprise_urls = os.getenv("APPRISE_URLS", "").split(",")
    if apprise_urls and apprise_urls != ['']:
        send_notification("Test Notification", "This is a test notification.", apprise_urls)
    else:
        print("APPRISE_URLS environment variable not set.")
