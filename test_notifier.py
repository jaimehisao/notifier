import unittest
from unittest.mock import patch, MagicMock
import os
import notifier
from click.testing import CliRunner

class TestNotifier(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        # Create a dummy config file for testing
        with open('test_config.yml', 'w') as f:
            f.write("""
channels:
  info:
    - mailto://user:pass@gmail.com
  warnings:
    - tgram://bottoken/chatid
""")

    def tearDown(self):
        os.remove('test_config.yml')

    @patch('notifier.send_notification')
    def test_cli_send_success(self, mock_send_notification):
        """
        Test that the CLI send command calls send_notification with the correct arguments.
        """
        result = self.runner.invoke(notifier.cli, [
            'send',
            '--title', 'Test Title',
            '--body', 'Test Body',
            '--channel', 'info',
            '--config', 'test_config.yml'
        ])
        self.assertEqual(result.exit_code, 0)
        mock_send_notification.assert_called_once_with(
            'Test Title',
            'Test Body',
            ['mailto://user:pass@gmail.com']
        )


class TestNotifier(unittest.TestCase):

    @patch('apprise.Apprise')
    def test_send_notification_success(self, mock_apprise):
        """
        Test that send_notification returns True on successful notification.
        """
        mock_apprise_instance = mock_apprise.return_value
        mock_apprise_instance.notify.return_value = True

        urls = ["mailto://user:pass@gmail.com"]
        result = notifier.send_notification("Test", "Test", urls)
        self.assertTrue(result)
        mock_apprise_instance.add.assert_called_once_with(urls[0])
        mock_apprise_instance.notify.assert_called_once_with(body="Test", title="Test")

    @patch('apprise.Apprise')
    def test_send_notification_failure(self, mock_apprise):
        """
        Test that send_notification returns False on failed notification.
        """
        mock_apprise_instance = mock_apprise.return_value
        mock_apprise_instance.notify.return_value = False

        urls = ["mailto://user:pass@gmail.com"]
        result = notifier.send_notification("Test", "Test", urls)
        self.assertFalse(result)
        mock_apprise_instance.add.assert_called_once_with(urls[0])
        mock_apprise_instance.notify.assert_called_once_with(body="Test", title="Test")

    @patch('logging_loki.LokiHandler')
    @patch('apprise.Apprise')
    def test_loki_logging_success(self, mock_apprise, mock_loki_handler):
        """
        Test that a successful notification is logged to Loki.
        """
        os.environ['LOKI_URL'] = 'http://localhost:3100/loki/api/v1/push'

        mock_apprise_instance = mock_apprise.return_value
        mock_apprise_instance.notify.return_value = True

        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            # Re-import notifier to re-evaluate the logger configuration
            import importlib
            importlib.reload(notifier)

            urls = ["mailto://user:pass@gmail.com"]
            notifier.send_notification("Test", "Test", urls)

            mock_logger.info.assert_called_once()

        del os.environ['LOKI_URL']
        importlib.reload(notifier)


    @patch('logging_loki.LokiHandler')
    @patch('apprise.Apprise')
    def test_loki_logging_failure(self, mock_apprise, mock_loki_handler):
        """
        Test that a failed notification is logged to Loki.
        """
        os.environ['LOKI_URL'] = 'http://localhost:3100/loki/api/v1/push'

        mock_apprise_instance = mock_apprise.return_value
        mock_apprise_instance.notify.return_value = False

        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            # Re-import notifier to re-evaluate the logger configuration
            import importlib
            importlib.reload(notifier)

            urls = ["mailto://user:pass@gmail.com"]
            notifier.send_notification("Test", "Test", urls)

            mock_logger.error.assert_called_once()

        del os.environ['LOKI_URL']
        importlib.reload(notifier)

if __name__ == '__main__':
    unittest.main()
