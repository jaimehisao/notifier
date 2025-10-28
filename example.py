import os
from notifier import send_notification

# This script demonstrates how to use the send_notification function
# from the notifier module.

# Before running this script, make sure to set the following environment
# variables in a .env file or in your shell:

# APPRISE_URLS: A comma-separated list of Apprise URLs.
# For example: "mailto://user:pass@gmail.com,tgram://bottoken/chatid"

# LOKI_URL: The URL of your Loki instance's push API endpoint.
# For example: "http://localhost:3100/loki/api/v1/push"

if __name__ == "__main__":
    apprise_urls = os.getenv("APPRISE_URLS", "").split(",")
    if apprise_urls and apprise_urls != ['']:
        # Define the title and body of the notification
        notification_title = "Example Notification"
        notification_body = "This is an example notification sent from the example.py script."

        # Send the notification
        send_notification(notification_title, notification_body, apprise_urls)
    else:
        print("APPRISE_URLS environment variable not set.")
        print("Please set it in a .env file or in your shell.")
