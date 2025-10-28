# Notifier

A simple notification system that uses Apprise to send notifications to various services and logs them to a Loki instance.

## Features

-   **Multi-service Notifications:** Uses Apprise to support a wide range of notification services like email (Gmail), Telegram, Slack, and more.
-   **Loki Logging:** Logs all outgoing notifications to a Loki instance for easy storage, searching, and monitoring.
-   **Configuration via Environment Variables:** Easily configure the system using a `.env` file.

## Requirements

-   Python 3.x
-   Dependencies listed in `requirements.txt`

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd notifier
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure your environment:**
    -   Create a `.env` file in the root of the project. You can copy the provided example:
    -   Open the `.env` file and add your configuration.

    **`.env` file example:**
    ```
    # Apprise URLs - comma-separated list of notification services
    # See Apprise documentation for URL formats: https://github.com/caronc/apprise
    # Example for Gmail and Telegram:
    # APPRISE_URLS="mailto://your_email:your_password@gmail.com,tgram://YourBotToken/YourChatID"
    APPRISE_URLS=""

    # Loki URL for logging
    # Example:
    # LOKI_URL="http://localhost:3100/loki/api/v1/push"
    LOKI_URL=""
    ```

## Usage

Once you have set up your `.env` file with the necessary `APPRISE_URLS` and `LOKI_URL`, you can send notifications.

### Running the Example

An example script `example.py` is provided to demonstrate how to use the notifier.

```bash
python example.py
```

This will send a test notification to the services you configured in your `.env` file and log the action to Loki.

### Integrating into Your Project

You can import the `send_notification` function from the `notifier.py` script into your own Python projects.

```python
from notifier import send_notification

# Your list of Apprise URLs (can also be loaded from environment variables)
urls = ["mailto://user:pass@gmail.com"]

title = "Important Update"
body = "This is a message from your application."

send_notification(title, body, urls)
```

## How It Works

-   **`notifier.py`**: This is the core script containing the `send_notification` function. It initializes `apprise` with the URLs provided and sends the message. It also configures a `python-logging-loki` handler to send logs to your Loki instance.
-   **`.env`**: This file stores your secret keys and configuration variables. It is loaded by `python-dotenv` at runtime.
-   **`example.py`**: A simple script showing how to call `send_notification`.
-   **`requirements.txt`**: A list of all the Python packages required for this project to run.
