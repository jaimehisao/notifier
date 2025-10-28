import os
import apprise
import logging
import logging_loki
from dotenv import load_dotenv

load_dotenv()

# Configure Loki logger
loki_url = os.getenv("LOKI_URL", "")
if loki_url:
    handler = logging_loki.LokiHandler(
        url=loki_url,
        tags={"application": "notifier"},
        version="1",
    )
    logger = logging.getLogger("notifier")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def send_notification(title, body, urls):
    """
    Sends a notification to the specified Apprise URLs.
    """
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
