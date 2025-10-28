# Notifier

A simple notification system that uses Apprise to send notifications to various services and logs them to a Loki instance.

## Features

-   **Multi-service Notifications:** Uses Apprise to support a wide range of notification services like email (Gmail), Telegram, Slack, and more.
-   **Loki Logging:** Logs all outgoing notifications to a Loki instance for easy storage, searching, and monitoring.
-   **Channel-based Configuration:** Configure notification channels in a `config.yml` file.
-   **Command-Line Interface (CLI):** Send notifications from the command line.
-   **Docker Support:** Run the notifier in a Docker container.

## Requirements

-   Python 3.x
-   Docker (optional)
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
    -   Create a `config.yml` file in the root of the project. You can copy the provided example:
    -   Open the `config.yml` file and add your configuration.

    **`config.yml` file example:**
    ```yaml
    # Notifier Configuration
    channels:
      info:
        - mailto://your_email:your_password@gmail.com
      warnings:
        - tgram://YourBotToken/YourChatID
      critical:
        - slack://tokenA/tokenB/tokenC
        - mailto://your_email:your_password@gmail.com
    ```

4.  **(Optional) Configure Loki:**
    -   Create a `.env` file and add your `LOKI_URL`.
    ```
    # Loki URL for logging
    LOKI_URL="http://localhost:3100/loki/api/v1/push"
    ```

## Usage

### Using the CLI

You can send notifications using the `send` command.

```bash
python notifier.py send --title "Hello" --body "This is a test" --channel "info"
```

### Using Docker

The notifier is also available as a Docker image.

```bash
# Build the Docker image
docker build -t notifier .

# Run the notifier using the Docker image
docker run -v $(pwd)/config.yml:/app/config.yml notifier send --title "Hello" --body "This is a test" --channel "info"
```

## How It Works

-   **`notifier.py`**: The core script, which uses `click` to provide the CLI and `apprise` to send notifications.
-   **`config.yml`**: The configuration file for defining notification channels.
-   **`Dockerfile`**: The file used to build the Docker image.
-   **`.drone.yml`**: The CI/CD pipeline configuration for Drone.
-   **`test_notifier.py`**: Unit tests for the notifier.
-   **`requirements.txt`**: A list of all the Python packages required for this project to run.
